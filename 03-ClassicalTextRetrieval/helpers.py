from IPython.display import display, Markdown, display_markdown
from tabulate import tabulate
from itertools import islice
import re
from collections import defaultdict, Counter
from nltk.stem import PorterStemmer
from PyPDF2 import PdfReader
from unidecode import unidecode

stopwords = { 
    "english": {'a',  'about', 'above', 'after', 'again', 'against', 'ain', 'all', 'am', 'an', 
                'and', 'any', 'are', 'aren', "aren't", 'as', 'at', 'be', 'because', 'been', 
                'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can', 'couldn', 
                "couldn't", 'd', 'did', 'didn', "didn't", 'do', 'does', 'doesn', "doesn't", 
                'doing', 'don', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 
                'further', 'had', 'hadn', "hadn't", 'has', 'hasn', "hasn't", 'have', 'haven', 
                "haven't", 'having', 'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 
                'his', 'how', 'i', 'if', 'in', 'into', 'is', 'isn', "isn't", 'it', "it's", 
                'its', 'itself', 'just', 'll', 'm', 'ma', 'me', 'mightn', "mightn't", 'more', 
                'most', 'mustn', "mustn't", 'my', 'myself', 'needn', "needn't", 'no', 'nor', 
                'not', 'now', 'o', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'our', 
                'ours', 'ourselves', 'out', 'over', 'own', 're', 's', 'same', 'shan', "shan't", 
                'she', "she's", 'should', "should've", 'shouldn', "shouldn't", 'so', 'some', 
                'such', 't', 'than', 'that', "that'll", 'the', 'their', 'theirs', 'them', 
                'themselves', 'then', 'there', 'these', 'they', 'this', 'those', 'through', 
                'to', 'too', 'under', 'until', 'up', 've', 'very', 'was', 'wasn', "wasn't", 
                'we', 'were', 'weren', "weren't", 'what', 'when', 'where', 'which', 'while', 
                'who', 'whom', 'why', 'will', 'with', 'won', "won't", 'wouldn', "wouldn't", 
                'y', 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 
                'yourselves'}
}


def print_table(rows: list[list[str]], headers: list[str], max_rows: int = 100, format: str = 'pipe'):
    if not rows or not headers: return
    if format == 'text':
        print(tabulate(islice(rows, max_rows), headers, tablefmt='github'))
    else:
        display(Markdown(tabulate(islice(rows, max_rows), headers, tablefmt=format)))

def extract_text_from_pdf(file_name: str) -> str:
    pages = []

    def visitor_text(text, cm, tm, fontDict, fontSize):
        y = tm[5]
        if y > 20 and len(text) > 0:
            # replace \n and multiple spaces (\s*) with a single space
            text = text.replace("\n", " ")
            text = re.sub(r'\[\d+\]|➢|•', '', text)
            parts.append(text)

    # read the PDF and extract all texts (do some post-processing with above function)
    reader = PdfReader(file_name)
    for page in reader.pages:
        parts = []
        page.extract_text(visitor_text=visitor_text)
        pages.append(re.sub(r'\s+',' ', " ".join(parts)).strip())

    # merge text blocks and clean-up
    return pages

def bag_of_words(tokens):
    terms = dict(Counter(tokens))
    return dict(terms.items())

def set_of_words(tokens):
    return set(tokens)

def tokenize(text: str) -> list[str]:
    text = re.sub(r'[^\w\-]+', ' ', text)
    tokens = []
    for token in text.split(' '):
        token = unidecode(token.strip().lower())
        if len(token) < 2: continue
        if not(re.match(r'^[a-zA-Z][\w\-\.]*$', token)): continue
        tokens.append(token)
    return tokens

porter_stemmer = PorterStemmer()

def reduce_to_stems(tokens):
    return list(map(lambda token: porter_stemmer.stem(token), tokens))

def eliminate_stopwords(tokens):
    return [token for token in tokens if not(token in stopwords['english'])]


# Boolean retrieval helpers
# ----------------------------------------

class BooleanRetriever:
    def __init__(self, collection: list[dict] = None, remove_stopwords: bool = True):
        self.remove_stopwords = remove_stopwords
        self.build_index(collection or [])
    
    def add_document(self, doc: dict):
        self.n_docs += 1
        doc_id = doc['docId'] = self.n_docs
        self.documents[doc_id] = doc
        # create vector from str-properties
        text = ' '.join([value for key, value in doc.items() if type(value) == str])
        tokens = tokenize(text)
        if self.remove_stopwords: tokens = eliminate_stopwords(tokens)
        tokens = reduce_to_stems(tokens)
        vector = doc['vector'] = set_of_words(tokens)
        # add to vocabulary and postings
        for term in vector:
            self.vocabulary[term] += 1
            self.index[term].add(doc_id)
    
    def build_index(self, collection: list[dict]):
        self.n_docs = 0
        self.documents = {}
        self.index = defaultdict(set)
        self.vocabulary = defaultdict(int)
        # load all documents
        for doc in collection:
            self.add_document(doc)
        self.n_terms = len(self.vocabulary)
        self.all = set(self.documents.keys())

    class BooleanExpression:
        pass

    class Term(BooleanExpression):
        """
            Boolean expression class for atomic term queries. For simplicity, we
            have all postings in memory but in real implementations, we would
            fetch the data from a file or database
        """
        def __init__(self, term: str, postings: list[int]):
            self.term = term
            self.postings = sorted(postings)

        def __iter__(self):
            return self.retrieve()
        
        # we used this flag to monitor which postings we fetch
        LOG_ACCESS = False

        def retrieve(self):
            for posting in self.postings:
                if BooleanRetriever.Term.LOG_ACCESS: print(f'{self.term}: {posting}')
                yield posting

    class Not(BooleanExpression):
        """
            Marker class for NOT operator on sub-expression. The retrieve method raises an exception.
            When used during AND operation, the retrieve method of the sub-expression is called.
        """
        def __init__(self, expression):
            self.expression = expression
        
        def __iter__(self):
            return self.retrieve()

        def retrieve(self):
            raise Exception("NOT operator not allowed at top-level of query")

    class And(BooleanExpression):
        """
            AND-expression with multiple sub-expressions. This operator can handle NOT(expr)-type 
            subexpressions and implements the correct '-' semantics of "cat AND NOT dog".
        """
        def __init__(self, *expressions):
            self.expressions = expressions

            # select expressison that are not Term or that have x._not = False
            self.pos = [e for e in expressions if not isinstance(e, BooleanRetriever.Not)]
            self.neg = [e for e in expressions if isinstance(e, BooleanRetriever.Not)]

        def __iter__(self):
            return self.retrieve()

        def retrieve(self):
            # streams for sub expressions without NOT
            # pos_iters contains the iterators for each sub expression
            # pos_nexts contains the next posting for each sub expression
            pos_iters = [iter(e) for e in self.pos]
            pos_nexts = [next(e, None) for e in pos_iters]

            # stream for sub expressions with NOT
            # neg_iters contains the iterators for each sub expression
            # neg_nexts contains the next posting for each sub expression
            neg_iters = [iter(e.expression) for e in self.neg]
            neg_nexts = [next(e, None) for e in neg_iters]

            # iterate until one pos_nexts element is None
            while None not in pos_nexts:
                # get smallest value from pos_nexts and neg_nexts, ignoring None values in neg_nexts
                smallest = min(pos_nexts + neg_nexts, key=lambda x: x if x is not None else float('inf'))

                # check if all entries of pos_nexts equal smallest, and no entry in neg_nexts equals smallest
                if all(e is smallest for e in pos_nexts) and smallest not in neg_nexts:
                    yield smallest
                
                # for each entry in pos_nexts and neg_nexts, fetch next item if entry equals smallest
                for i, e in enumerate(pos_nexts):
                    if e is smallest:
                        pos_nexts[i] = next(pos_iters[i], None)
                for i, e in enumerate(neg_nexts):
                    if e is smallest:
                        neg_nexts[i] = next(neg_iters[i], None)

    class Or(BooleanExpression):
        """
            OR-expression with multiple sub-expressions. This operator cannot handle NOT(expr)-type subexpressions
        """
        def __init__(self, *expressions):
            # check that there are no NOT(expr)-type subexpressions
            if any(isinstance(e, BooleanRetriever.Not) for e in expressions):
                raise Exception("OR-expression cannot handle NOT(expr)-type subexpressions")
            self.expressions = expressions
        
        def __iter__(self):
            return self.retrieve()

        def retrieve(self):
            iters = [iter(e) for e in self.expressions]
            nexts = [next(e, None) for e in iters]

            while not all(e is None for e in nexts):
                # get smallest value from nexts, ignoring None values
                smallest = min(nexts, key=lambda x: x if x is not None else float('inf'))
                yield smallest
                
                # for each entry in nexts, fetch next item if entry equals smallest
                for i, e in enumerate(nexts):
                    if e is smallest:
                        nexts[i] = next(iters[i], None)


    @staticmethod
    def format_bool(expr: BooleanExpression) -> str:
        """
            Prints a Boolean expression in a human-readable format.
        """
        if isinstance(expr, BooleanRetriever.And):
            return '({})'.format(' AND '.join([BooleanRetriever.format_bool(e) for e in expr.expressions]))
        if isinstance(expr, BooleanRetriever.Or):
            return '({})'.format(' OR '.join([BooleanRetriever.format_bool(e) for e in expr.expressions]))
        if isinstance(expr, BooleanRetriever.Not):
            return f"NOT({BooleanRetriever.format_bool(expr.expression)})"
        return f"{expr.term}"

    def parse_query(self, query: str) -> BooleanExpression:
        """
            expression := term {"OR" term}
            term := factor {"AND" factor}
            factor := <word> | "NOT" factor | "(" expression ")"
        """
        def factor(tokens: list[str]):
            if not tokens: raise ValueError("parse error")
            if tokens[0] == '(':
                tokens.pop(0)
                expr = expression(tokens)
                if not tokens or tokens[0] != ')': raise ValueError("parse error")
                tokens.pop(0)
                return expr
            if tokens[0] == 'NOT':
                tokens.pop(0)
                return BooleanRetriever.Not(factor(tokens))
            term = tokens.pop(0)
            return BooleanRetriever.Term(term, self.index[term])

        def term(tokens: list[str]):
            expr = [factor(tokens)]
            if not tokens or tokens[0] != 'AND':
                return expr[0]
            while tokens and tokens[0] == 'AND':
                tokens.pop(0)
                expr.append(factor(tokens))
            return BooleanRetriever.And(*expr)    

        def expression(tokens: list[str]):
            expr = [term(tokens)]
            if not tokens or tokens[0] != 'OR': 
                return expr[0]
            while tokens and tokens[0] == 'OR':
                tokens.pop(0)
                expr.append(term(tokens))
            return BooleanRetriever.Or(*expr)

        tokens = re.findall(r"\w+|\(|\)", query)
        return expression(tokens)
    
    def search(self, query: str, logging: bool = False) -> list:
        BooleanRetriever.Term.LOG_ACCESS = logging
        return self.parse_query(query).retrieve()
    
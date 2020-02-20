import os

OUT_PATH = 'out'
SCORE_FILE = os.path.join(OUT_PATH, 'scores.txt')


class Book:
    def __init__(self, id_, score):
        self.id = id_
        self.score = score

    def __repr__(self):
        return f'{self.id}:{self.score}'


class Library:

    def __init__(self, id_, n_books, days, ship, books):
        self.id = id_
        self.n_books = n_books
        self.days = days
        self.remaining_days = days
        self.ship = ship
        self.books = books
        self.books_to_scan = [b for b in sorted(books, key=lambda x: x.score, reverse=True)]
        self.scanned_books = []

    def get_lib_score(self):
        return sum((book.score for book in self.books))

    def sign_up(self):
        return self.days

    def do(self):
        if self.remaining_days > 0:
            self.remaining_days -= 1
            return False

        return True

    def scan(self, books=None):
        scanning = self.books_to_scan[: self.ship]
        self.scanned_books.extend(scanning)
        self.books_to_scan = self.books_to_scan[self.ship:]
        return scanning

    def is_scanning(self):
        return len(self.books_to_scan) > 0

    def __repr__(self):
        return f'Lib(b={self.n_books} d={self.days} s={self.ship} bs={self.books} sc={self.get_lib_score()})'


def scan(file):
    print(f'Scanning file {file}')

    n_books, n_libs, n_days, scores, libs = read(file)
    print(f'Got {n_books} books, {n_libs} libraries and {n_days} days to work with.')

    ordered_libs = sorted([lib for lib in libs], key=lambda l: l.get_lib_score(), reverse=True)
    ordered_scores = sorted([(i, s) for i, s in enumerate(scores)], key=lambda x: x[1], reverse=True)

    scanning_libs = []
    scanner_libs = []
    scanned_books = set()

    n_scanning_libs = 0

    signing_lib = None

    for day in range(n_days):

        if signing_lib is None:
            signing_lib = ordered_libs.pop(0)

        if signing_lib.do():
            scanning_libs.append(signing_lib)
            scanner_libs.append(signing_lib)
            n_scanning_libs += 1
            signing_lib = None

        for lib in scanning_libs:
            scanned = lib.scan()
            scanned_books.update(scanned)
            if not lib.is_scanning():
                scanning_libs.remove(lib)

    print(f'Last day reached.')
    print(f'Scanned {len(scanned_books)} books in {n_days} days.')
    score = sum((b.score for b in scanned_books))
    print(f'Score for file {file}: {score}')

    write(file, n_scanning_libs, scanner_libs)

    with open(SCORE_FILE, 'a') as f:
        f.write(f'{file:<28} {score:>10}\n')


def write(file, n_scanning_libs, libs):
    if not os.path.exists(OUT_PATH):
        os.mkdir(OUT_PATH)
    with open(os.path.join(OUT_PATH, file), 'w') as f:
        f.write(str(n_scanning_libs))
        f.write('\n')
        for lib in libs:
            f.write(f'{lib.id} {len(lib.scanned_books)}')
            f.write('\n')
            f.write(' '.join((str(book.id) for book in lib.scanned_books)))
            f.write('\n')


def read(file):
    with open(f'in/{file}', 'r') as f:
        n_books, n_libs, n_days = [int(d) for d in f.readline().split()]
        scores = [int(d) for d in f.readline().split()]
        books = [Book(i, s) for i, s in enumerate(scores)]
        lines = [[int(d) for d in line.split()] for line in f.readlines()]
        # for (n_books, days, ship), books in zip(lines[0::2], lines[1::2]):
        #     books = {book: score for book, score in zip(books, scores)}
        #     libs.append(Library(n_books, days, ship, books))
        libs = [
            Library(id_, int(n_books), int(days), int(ship), [books[book_id] for book_id in book_ids])
            for id_, ((n_books, days, ship), book_ids) in enumerate(zip(lines[0::2], lines[1::2]))]

    return n_books, n_libs, n_days, scores, libs


if __name__ == '__main__':
    if os.path.exists(SCORE_FILE):
        os.remove(SCORE_FILE)
    scan('a_example.txt')
    scan('b_read_on.txt')
    scan('c_incunabula.txt')
    scan('d_tough_choices.txt')
    scan('e_so_many_books.txt')
    scan('f_libraries_of_the_world.txt')


class ChessBoard:

    unicode_pieces = {
        'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
        'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟', '.': ' '
    }

    def __init__(self, fen: str):
        self.board = self.parse_fen(fen)

    def parse_fen(self, fen: str) -> list:
        ranks = fen.split()[0].split('/') # Split the FEN string into ranks
        board = []

        for rank in ranks:
            board_rank = []
            for char in rank:
                empty_squares = char.isdigit()
                if empty_squares: # if the char in the fen is a num, it is an empty square so add that many empty squares
                    board_rank.extend(['.'] * int(char))
                else:
                    board_rank.append(char) # if the char is a piece, add it to the board
            board.append(board_rank)
    
        return board
    
    def print_board(self):
        """Print the board in a human-readable format using unicode characters"""

        print("\n     a  b  c  d  e  f  g  h")  # Column labels
        print("     ------------------------")
        for i, rank in enumerate(self.board):
            print(f'{8 - i} |', end='  ')
            for square in rank:
                print(self.unicode_pieces[square], end='  ')
            print(f'|{8 - i}')
     
        print("     ------------------------")
        print("      a  b  c  d  e  f  g  h")  # Column labels

if __name__ == '__main__':
    start_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    board = ChessBoard(start_fen)
    board.print_board()
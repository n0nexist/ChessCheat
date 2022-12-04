from rich import print
from rich.prompt import Prompt
from selenium import webdriver
from selenium.webdriver.common.by import By
import chess
import os

board = chess.Board()
os.environ['fen'] = board.fen()
os.system("clear")

class color:
    arrow = "[cyan]:[reset][bold red]"
    _list = "[bold italic cyan]· [reset][dim red]"

class utils:
    def parseboolean(b):
        return b.replace("True","[bold italic green]True").replace("False","[dim bold red]False")

class pychess:
    def update_fen():
        os.environ['fen'] = board.fen()

    def load_byfen(fen):
        board = chess.Board(fen)
        pychess.update_fen()
        print(board)

    def undo_lastmove():
        print(f"{color.arrow} cancelling last move made..")
        board.pop()
        pychess.update_fen()
        pychess.printfen()

    def printfen():
        print(f"{color.arrow} board's FEN is: [italic white]{os.getenv('fen')}")

    def status():
        pychess.printfen()
        print(board)
        print(f"{color.arrow} is checkmate[reset][white]: {utils.parseboolean(str(board.is_checkmate()))}")
        print(f"{color.arrow} is check[reset][white]: {utils.parseboolean(str(board.is_check()))}")
        print(f"{color.arrow} is insufficient material[reset][white]: {utils.parseboolean(str(board.is_insufficient_material()))}")
        print(f"{color.arrow} is possible draw[reset][white]: {utils.parseboolean(str(board.can_claim_draw()))}")
        print(f"{color.arrow} is game over[reset][white]: {utils.parseboolean(str(board.is_game_over()))}")
        print(f"{color.arrow} is white's turn[reset][white]: {utils.parseboolean(str(board.turn))}")

    def pushmove(from_,to_):
        move = from_+to_
        print(f"{color.arrow} pushing [reset][italic cyan]{from_}[reset][bold white]->[reset][italic cyan]{to_}[reset][dim red] on board..")
        if board.is_kingside_castling(chess.Move.from_uci(move)):
            print(f"{color.arrow} the move is a kingside castling")
        elif board.is_queenside_castling(chess.Move.from_uci(move)):
            print(f"{color.arrow} the move is a queenside castling")
        elif board.is_en_passant(chess.Move.from_uci(move)):
            print(f"{color.arrow} the move is an 'en passant'")
        elif board.is_capture(chess.Move.from_uci(move)):
            print(f"{color.arrow} the move is a capture")
        board.push_uci(move)
        pychess.update_fen()
        pychess.printfen()

    def legal_moves():
        print("[italic white]LEGAL MOVES:")
        for x in board.legal_moves:
            move = str(x)
            print(f"{color._list}[bold underline white]{move}[reset] [italic cyan]([reset][red]attacked by BLACK[reset]: {utils.parseboolean(str(board.is_attacked_by(chess.BLACK, x.to_square)))} - [reset][red]attacked by WHITE[reset]: {utils.parseboolean(str(board.is_attacked_by(chess.WHITE, x.to_square)))}")


class nextchessmove:
    def nextmove(fen):
        url = "https://nextchessmove.com?fen="+fen
        driver = webdriver.Firefox()
        driver.get(url)
        driver.find_element(By.XPATH, '//button[text()="Calculate Next Move"]').click()
        while True:
            string = "<button class=\"link\"><span>"
            try:
                a = driver.page_source.split(string)[1].split("</span>")[0]
                driver.quit()
                return a
            except:
                pass

class chch_main:
    def main():
        chch_main.logo()
        chch_main.loop()

    def loop():
        print("\n")
        while True:
            try:
                cmd = Prompt.ask(f"[bold white]h4ck3r@chesscheat").lower()
                if cmd == "help":
                    print(f"""
{color._list}cls -> clears the screen
{color._list}loadfen -> loads new board code
{color._list}showfen -> shows current board code
{color._list}legalmoves -> shows legal moves
{color._list}wrender -> shows board layout for white
{color._list}brender -> shows board layout for black
{color._list}pushmove -> pushes a move in the board
{color._list}undo -> cancels last move made in the board
{color._list}status -> shows board status
{color._list}bestmove -> shows best possible move
{color._list}quit -> exits
                    """)
                elif cmd == "loadfen":
                    pychess.load_byfen(Prompt.ask("[bold white]FEN"))
                elif cmd == "cls":
                    os.system("clear")
                elif cmd == "showfen":
                    pychess.printfen()
                elif cmd == "legalmoves":
                    pychess.legal_moves()
                elif cmd == "wrender":
                    print(board)
                elif cmd == "brender":
                    print(board.mirror())
                elif cmd == "pushmove":
                    pychess.pushmove(Prompt.ask("[bold white]FROM"), Prompt.ask("[bold white]TO"))
                elif cmd == "undo":
                    pychess.undo_lastmove()
                elif cmd == "status":
                    pychess.status()
                elif cmd == "bestmove":
                    print(f"{color.arrow} retrieving [italic]best[/italic] possible move with FEN: [reset][italic white]{os.getenv('fen')}")
                    print(f"{color.arrow} the [italic]best[/italic] possible move to continue the match is: [reset][underline italic cyan]{nextchessmove.nextmove(os.getenv('fen'))}")
                elif cmd == "quit":
                    print("[italic cyan]goodbye[reset][bold white]!")
                    exit()
                else:
                    print(f"{color.arrow} unknown command. try 'help'")
                print("\n")
            except Exception as e:
                print(f"{color.arrow} python exception - [reset][bold underline cyan]{str(e)}")
                pass
            

    def logo():
        print("""[bold blue]
   ___ _       ___ _     
  / __\ |__   / __\ |__  
 / /  | '_ \ / /  | '_ \ 
/ /___| | | / /___| | | |
\____/|_| |_\____/|_| |_|
    (chess)   (cheat)

[white]>[italic cyan] made by n0nexist
        """)


chch_main.main()
import pyautogui        
import time
 
def click_points():
    # Obtém as coordenadas dos dois pontos onde deseja clicar
    point1_x, point1_y = 100, 200
    point2_x, point2_y = 300, 400
 
    while True:
        # Clica no primeiro ponto
        pyautogui.click(point1_x, point1_y)
        # Espera 0.5 segundos en20otre os cliques (opcional)
        time.sleep(0.5)
        # Clica no segundo ponto
        pyautogui.click(point2_x, point2_y)
        time.sleep(0.5)
        pyautogui.click(point1_x, point1_y)
        time.sleep(0.5)
        # Clica no segundo ponto'
        pyautogui.click(point2_x, point2_y)
        # Espera 10 segundos antes de repetir o ciclo
        time.sleep(10)
 
if __name__ == "__main__":
    click_points()
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class SocketServer {

    public static void main(String[] args) {
        try {
            // Определяем порт сервера
            int port = 1234;

            // Создаем серверный сокет для прослушивания подключений на указанном порту
            ServerSocket serverSocket = new ServerSocket(port);

            // Ожидаем подключения клиента
            Socket clientSocket = serverSocket.accept();

            // Создаем поток ввода для получения запроса от клиента
            BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));

            // Создаем поток вывода для отправки ответа клиенту
            PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);

            // Читаем запрос от клиента
            String request = in.readLine();
            System.out.println("Получен запрос от клиента: " + request);

            // Отправляем ответ клиенту
            out.println("Привет, клиент!");
            System.out.println("Отправлен ответ клиенту: Привет, клиент!");

            // Закрываем сокет
            clientSocket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

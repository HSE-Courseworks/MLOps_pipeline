import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class SocketClient {

    public static void main(String[] args) {
        try {
            // Определяем адрес и порт сервера
            String host = "127.0.0.1";
            int port = 1234;

            // Создаем сокет для подключения к серверу
            Socket socket = new Socket(host, port);

            // Создаем поток вывода для отправки запроса на сервер
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);

            // Создаем поток ввода для получения ответа от сервера
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            // Отправляем запрос на сервер
            out.println("Привет, сервер!");

            // Получаем ответ от сервера
            String response = in.readLine();

            // Выводим ответ на консоль
            System.out.println("Ответ от сервера: " + response);

            // Закрываем сокет
            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

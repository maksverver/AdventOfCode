import java.io.*;
import java.util.*;

class Day15 {
    private static final int DR[] = {-1, 0, 0, 1};
    private static final int DC[] = {0, -1, 1, 0};

    /** Priority queue element (row, col, total distance) */
    private static class Elem implements Comparable<Elem> {
        final int r, c, d;

        Elem(int r, int c, int d) {
            this.r = r;
            this.c = c;
            this.d = d;
        }

        @Override
        public int compareTo(Elem other) {
            return Integer.compare(d, other.d);
        }
    }

    static int solve(int H, int W, int [][] danger) {
        // Dijkstra's algorithm.
        final int[][] minDist = new int[H][W];
        for (int r = 0; r < H; ++r) {
            for (int c = 0; c < W; ++c) {
                minDist[r][c] = Integer.MAX_VALUE;
            }
        }
        final PriorityQueue<Elem> todo = new PriorityQueue<>();
        minDist[0][0] = 0;
        todo.add(new Elem(0, 0, 0));
        while (!todo.isEmpty()) {
            Elem e = todo.poll();
            int r = e.r;
            int c = e.c;
            int d = e.d;
            if (d != minDist[r][c]) {
                continue;
            }
            if (r == H - 1 && c == W - 1) {
                return d;
            }
            for (int dir = 0; dir < 4; ++dir) {
                int r2 = r + DR[dir];
                int c2 = c + DC[dir];
                if (0 <= r2 && r2 < H && 0 <= c2 && c2 < W) {
                    int d2 = d + danger[r2][c2];
                    if (d2 < minDist[r2][c2]) {
                        minDist[r2][c2] = d2;
                        todo.add(new Elem(r2, c2, d2));
                    }
                }
            }
        }
        return -1;
    }

    public static void main(String... args) {
        final ArrayList<String> lines = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(System.in))) {
            for (String line; (line = reader.readLine()) != null; ) {
                lines.add(line);
            }
        } catch (IOException e) {
            System.err.println("Failed to read input! " + e);
            return;
        }
        int H = lines.size();
        int W = lines.get(0).length();
        int[][] danger = new int[H][W];
        for (int r = 0; r < H; ++r) {
            for (int c = 0; c < W; ++c) {
                danger[r][c] = lines.get(r).charAt(c) - '0';
            }
        }

        // Part 1
        System.out.println(solve(H, W, danger));

        // Part 2
        int[][] danger2 = new int[H*5][W*5];
        for (int r = 0; r < H*5; ++r) {
            for (int c = 0; c < W*5; ++c) {
                danger2[r][c] = (danger[r % H][c % W] - 1 + (r / H) + (c / W)) % 9 + 1;
            }
        }
        System.out.println(solve(H*5, W*5, danger2));
    }
}

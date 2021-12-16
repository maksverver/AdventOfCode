import java.io.*;
import java.util.*;

class Day15NoPQ {
    private static final int DR[] = {-1, 0, 0, 1};
    private static final int DC[] = {0, -1, 1, 0};

    private static class Coords {
        final int r, c;

        Coords(int r, int c) {
            this.r = r;
            this.c = c;
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
        final ArrayList<ArrayList<Coords>> q = new ArrayList<>();
        q.add(new ArrayList<>());
        minDist[0][0] = 0;
        q.get(0).add(new Coords(0, 0));
        for (int d = 0; d < q.size(); ++d) {
            for (Coords e : q.get(d)) {
                int r = e.r;
                int c = e.c;
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
                            while (q.size() <= d2) {
                                q.add(new ArrayList<>());
                            }
                            q.get(d2).add(new Coords(r2, c2));
                        }
                    }
                }
            }
            q.set(d, null);
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

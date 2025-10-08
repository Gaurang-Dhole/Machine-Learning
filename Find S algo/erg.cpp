#include <bits/stdc++.h>

using namespace std;

vector<vector<char>> board(8, vector<char>(8));

bool isvalid(int row, int col)
{

    for (int i = 0; i < row; i++)

        if (board[i][col] == '1')
            return false;

    for (int i = row - 1, j = col - 1; i >= 0 && j >= 0; i--, j--)
    {
        if (board[i][j] == '1')
            return false;

        for (int i = row - 1, j = col + 1; i >= 0 && j < 8; i--, j++)

            if (board[i][j] == '1')
                return false;

        return true;
    }

    int rem(int lev)
    {

        if (lev == 8)
            return 1;

        int ans = 0;

        for (int i = 0; i < 8; i++)
        {

            if (board[lev][i] == '.' && isvalid(lev, i))
            {

                board[lev][i] = '1';

                ans += rem(lev + 1);

                board[lev][i] = '.';
            }
        }

        return ans;
    }

    int main()
    {

        ios_base::sync_with_stdio(false);

        cin.tie(0);

        cout.tie(0);

        for (int i = 0; i < 8; i++)

            for (int j = 0; j < 8; j++)

                cin >> board[i][j];

        cout << rem(0) << endl;
    }
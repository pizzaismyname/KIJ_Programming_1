#include <bits/stdc++.h>
using namespace std;

string key;
char grid[5][5], words[10000];
vector<pair<char, char>> digraph;

void inputKey()
{
    cout << "Masukkan key: ";
    cin >> key;
    int len = key.length();
    for (int i = 0; i < len; i++)
    {
        key[i] = toupper(key[i]);
    }
}

void generateKeySquare()
{
    char ch = 'A';
    int count = 0;
    int len = key.length();
    set<char> dup;
    pair<set<char>::iterator, bool> stat;
    for (int i = 0; i < 5; i++)
    {
        for (int j = 0; j < 5; j++)
        {
            if (count < len)
            {
                stat = dup.insert(key[count]);
                if (stat.second && ch != 'J')
                {
                    grid[i][j] = key[count];
                }
                else
                {
                    j--;
                }
                count++;
            }
            else
            {
                stat = dup.insert(ch);
                if (stat.second && ch != 'J')
                {
                    grid[i][j] = ch;
                }
                else
                {
                    j--;
                    ch++;
                }
            }
        }
    }
    cout << "\nCipher Key Square:\n";
    for (int i = 0; i < 5; i++)
    {
        for (int j = 0; j < 5; j++)
        {
            cout << grid[i][j] << " ";
        }
        cout << endl;
    }
    cout << endl;
}

void readPlaintext()
{
    char ch = '\0';
    int index = 0;
    cout << "Masukkan nama file untuk dienkripsi (dan ekstensi): ";
    string filename;
    cin >> filename;
    ifstream plaintext;
    plaintext.open(filename);
    while (plaintext >> ch)
    {
        if (ch == ' ' || ch == '\n')
        {
            continue;
        }
        if (ch == 'j' || ch == 'J')
        {
            ch = 'i';
        }
        words[index] = toupper(ch);
        index++;
    }
    plaintext.close();
}

void splitToDigraphs()
{
    char ch = words[0];
    int len = strlen(words);
    for (int i = 1; i < len; i++)
    {
        if (words[i] != ch)
        {
            digraph.push_back({ch, words[i]});
            i++;
        }
        else
        {
            digraph.push_back({ch, 'X'});
        }
        ch = words[i];
        if (i == len - 1)
        {
            digraph.push_back({words[i], 'X'});
        }
    }
}

void encrypt()
{
    int x1, y1, x2, y2;
    for (int i = 0; i < digraph.size(); i++)
    {
        for (int j = 0; j < 5; j++)
        {
            for (int k = 0; k < 5; k++)
            {
                if (grid[j][k] == digraph[i].first)
                {
                    x1 = j;
                    y1 = k;
                }
                if (grid[j][k] == digraph[i].second)
                {
                    x2 = j;
                    y2 = k;
                }
            }
        }
        if (x1 == x2)
        {
            digraph[i].first = grid[x1][(y1 + 1) % 5];
            digraph[i].second = grid[x2][(y2 + 1) % 5];
        }
        else if (y1 == y2)
        {
            digraph[i].first = grid[(x1 + 1) % 5][y1];
            digraph[i].second = grid[(x2 + 1) % 5][y2];
        }
        else
        {
            digraph[i].first = grid[x1][y2];
            digraph[i].second = grid[x2][y1];
        }
    }
}

void writeCiphertext()
{
    ofstream ciphertext;
    ciphertext.open("cipher.txt");
    for (int i = 0; i < digraph.size(); i++)
    {
        ciphertext << digraph[i].first << digraph[i].second;
    }
    ciphertext.close();
}

int main()
{
    inputKey();
    generateKeySquare();
    readPlaintext();
    splitToDigraphs();
    encrypt();
    writeCiphertext();
    return 0;
}

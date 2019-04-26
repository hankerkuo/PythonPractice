#include <stdio.h>
#include <stdlib.h>

void hanoi(int, char, char, char);

// time計數用而已
int time = 0;

int main(void)
{
    int n;

    printf("請輸入河內塔的高度：");
    scanf("%d", &n);

    hanoi(n, 'A', 'B', 'C');

    printf("移動 %d 層河內塔共需移動 %d 次\n", n, time);

    system("pause");
}

// 函數的引數ABC代表甚麼意義?
// A -> 塔的起始位置, B -> 塔的中繼位置, C -> 塔最後移動到的位置
void hanoi(int n, char A, char B, char C)
{
    // 遞迴終止條件 當塔的積木只有1塊 直接把它從A搬到C
    if (n == 1)
    {
        printf("%d: 將第 %d 個圓盤由 %c 移到 %c\n", ++time, n, A, C);
    }
    // 若塔高度不是1 則進行遞迴
    else
    {
        // 下方遞迴順序變成ACB的原因
        // 欲把N-1層以上的塔先從A搬到B, 因此 起始:A, 中繼:C, 最後位置:B -> A, C, B
        hanoi(n - 1, A, C, B);
        // 下方這行把最底層(N層)的積木從A搬到C
        printf("%d: 將第 %d 個圓盤由 %c 移到 %c\n", ++time, n, A, C);
        // 下方遞迴順序變成BAC的原因
        // 欲把N-1層以上的塔從B搬到C, 因此 起始:B, 中繼:A, 最後位置:C -> B, A, C
        hanoi(n - 1, B, A, C);
    }
}
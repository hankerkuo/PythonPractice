#include "stdio.h"
#include "string.h"

//參數說明:str:輸入字串, show:用以儲存欲印出的排列組合, str_length:輸入字串的長度
void permutation(char str[100], char show[100], unsigned int str_length){
// 必備的遞迴終止條件 當(show)的字串長度=輸入字串的長度 印出結果
 if (strlen(show) == str_length){
     for(int i = 0; i < str_length; i++){
       printf("%c", show[i]);
      }
     printf("\n");
 }
 else{
// 變換輸入字串(str)的第一個字元
 for (unsigned int i = 0; i < strlen(str); i++){
    //str_temp 與 show_temp 用來傳送結果給下一層遞迴 先宣告
     char str_temp[100] = "";
     char show_temp[100] = "";
    //strcpy 函式複製show到show_temp
     strcpy(show_temp, show);
    //挑出第i個字元放到show_temp裡面
     show_temp[strlen(show)] = str[i];
    //重點部分!! 把已經挑出來的第i個字元去除掉
     int count = 0;
     for(unsigned int j = 0; j < strlen(str); j++){
         if(j == i) continue;
         str_temp[count] = str[j];
         count ++;
      }
    //接著丟入下一層遞迴
     permutation(str_temp, show_temp, str_length);
     }
 }
}


int main()
{
  //欲求不同字串的排列組合 修改str[100]就好
  //如果字串長度超過100, 則字串宣告中的[100]自己調整
  char str[100] ="xyz";
  char show[100] = "";
  unsigned int str_length = strlen(str);
  permutation(str, show, str_length);
  return 0;
}

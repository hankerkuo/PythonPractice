#include "stdio.h"
#include "string.h"

// permutation function
void permutation(char str[100], char show[100], unsigned int str_length){
 if (strlen(show) == str_length){
     for(int i = 0; i < str_length; i++){
       printf("%c", show[i]);
      }
     printf("\n");
 }
 else{
 for (unsigned int i = 0; i < strlen(str); i++){
     char str_temp[100] = "";
     char show_temp[100] = "";

     strcpy(show_temp, show);
     show_temp[strlen(show)] = str[i];

     int count = 0;
     for(unsigned int j = 0; j < strlen(str); j++){
         if(j == i) continue;
         str_temp[count] = str[j];
         count ++;
      }
     permutation(str_temp, show_temp, str_length);
     }
 }
}

int main()
{
  char str[100] ="xyz";
  char show[100] = "";
  unsigned int str_length = strlen(str);
  permutation(str, show, str_length);
  system("pause");
  return 0;
}

#include <iostream>
#include <fstream>

using namespace std;

char cyfry, wybor;
string nazwa_pliku_odczyt, nazwa_pliku_zapis;
void zapis_fun();
int main()
{
    cout<<"Podaj nazwe pliku z ktorego chcesz odczytac (np. plik.txt): "<<endl;
    cin>>nazwa_pliku_odczyt;
    ifstream odczyt_pliku(nazwa_pliku_odczyt);
    while(!odczyt_pliku)
    {
        cout<<"Podany plik nie istnieje, Podaj poprawna nazwe:"<<endl;
        cin>>nazwa_pliku_odczyt;
        odczyt_pliku.open(nazwa_pliku_odczyt);
    }
    cout<<"Plik Poprawny"<<endl;

    zapis_fun();
    while(wybor == 'n' || wybor=='N')
    {
        zapis_fun();
    }
    ofstream zapis_pliku(nazwa_pliku_zapis);
    while (odczyt_pliku.get(cyfry))
    {
        if (cyfry != ')' && cyfry != '(' && cyfry != '\'' && cyfry != ';')
        {
          zapis_pliku << cyfry;
        }

    }
    odczyt_pliku.close();
    zapis_pliku.close();
    cout<<"Zrobione!"<<endl;
}
inline void zapis_fun()
{
    cout<<"Podaj nazwe pliku do ktorego chcesz zapisac (np. plik.txt): "<<endl;
    cin>>nazwa_pliku_zapis;
    cout<<"Czy do tego pliku: "<<nazwa_pliku_zapis<<" chcesz zapisac dane? (T-tak, N-nie)"<<endl;
    cin>>wybor;
}

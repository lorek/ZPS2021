# ZPS2021
Zespołowy Projekt Specjalnościowy 2021

 
# Materialy
Część materiałów dostępna jest w Moodle (link: TBA)

Tutaj powinny się pojawić skrypty niezbędne do wykonania projektu.

# Windows: git bash
To dotyczy tylko windowsa: trzeba zainstalowac [Git Bash](https://git-scm.com/downloads)
Tutaj sa tez jakies filmiki: [Link 1](https://www.youtube.com/watch?v=rWboGsc6CqI), [Link 2](https://www.youtube.com/watch?v=9bJkPb9HfuA)

# Pobranie repozytorium
Bedziemy korzystali z repozytorium [https://github.com/lorek/ZPS2021](https://github.com/lorek/ZPS2021)

Stworzmy katalog `repos`, do ktorego sciagniemy powyzsze repozytorium:

Pierwsze pobranie repozytorium:
```
$ mkdir repos
$ cd repos
$ git clone https://github.com/lorek/ZPS2021.git
$ cd ZPS2021
```

# Stworzenie konta na GitHub, pierwszy commit i push
Jak widac powyzej - kazdy moze sciagnac nasze repozytorium, stosowne uprawnienia sa natomiast niezbedne do pisania w repozytorium

*  **Zalozenie konta**

Nalezy na stronie [https://github.com](https://github.com) zalozyc konto oraz koniecznie 
[zweryfikowac adres email](https://github.com/settings/emails)

*  **Dolaczenie do wspolpracownikow projektu**

Prosze na stronie projektu w zakladce "Issues", tj. pod adresem [https://github.com/lorek/ZPS2021/issues](https://github.com/lorek/ZPS2021/issues) wpisac "issue" z informacja o nazwie uzytkownika (jest tam podany przyklad - jest to cos typu forum, po prostu tutaj bede widzial kto z Was zalozyl konto i jaka ono ma nazwe)

*  **Akceptacja 'zaproszenia'**

Wszystkim, którzy sie wpisza na [https://github.com/lorek/ZPS2021/issues](https://github.com/lorek/ZPS2021/issues)  (i podadza nazwe uzytkownika) wyślę tzw. "zaproszenie", które nalezy zaakceptowac (od wtedy bedzie sie pelnoprawnym 'wspolpracownikiem' - zaproszenie powinno przyjsc mailem, mozna tez zobaczyc "Notifications" = 'dzwonek' w prawym gornym rogu)

Po tym, jak dodam uzytkownika jako "wspolpracownika" mozna nadpisywac/dodawac pliki. 
Mozliwe, ze jest tez wymagane ustawienie zmiennych `user.name` oraz `user.email`, co robimy komendami (raz to robimy):

```
$ git config --global user.name "Jan Kowalski"
$ git config --global user.email "Jan.Kowalski@mail.com"
```

`ZADANIE`: 
* Prosze wowczas w pliku `users.txt` dopisac swoja nazwe uzytkownia
* W katalogu `users_test/` stworzyc plik o nazwie `nazwa_uzytkownika.txt`
* Nastepnie prosze te zmiany wgrac do repozytorium:

```
$ git add users.txt
$ git add users_test/nazwa_uzytkownika.txt
$ git commit -m 'Zauktalizowany plik users.txt i dodany users_test/nazwa_uzytkownika.txt'
$ git push
```

Powinien on wowczas spytac o login i haslo uzytkownika.

Najważniejsze operacje: a) dodawanie pliku (jak wyżej); b) ściąganie najnowszej wersji repozytorium: `git pull`



*  **Używanie kluczy SSH**

Ten punkt nie jest obowiązkowy, ale ułatwia pracę. Jeśli wykonałeś tylko powyższe kroki, przy każdym `git push` niezbędne będzie podawanie hasła. Wygodniejsza jest autoryzacja za pomocą kluczy ssh. Poniższe dotyczy systemu Linux. 

Generowanie klucza (typowe opcje):
```
$ ssh-keygen -t rsa -b 4096 -C "Jan.Kowalski@mail.com" 
```
Po tej instrukcji w podkatalogu (w katalogu domowym) `.ssh` powinny znaleźć się 2 pliki: `id_rsa` (klucz prywatny) oraz `id_rsa.pub` (klucz publiczny). 
Teraz należy na swoim koncie na GitHub dodać  klucz publiczny:
`Settings -> SSH and GPG keys -> SSH keys -> New SSH key`

Od tej pory powinniśmy móc pisać do repozytorium bez podawania hasła.



 

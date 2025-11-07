I learned the story of how Andrey Markov argued with Pavel Nekrasov about the importance of studying dependent random variables and the Law of Large Numbers for them. 
In the process, he came up with the concept of Markov chains, and to test his marginal distribution theorem in practice, 
he took a text of "Eugene Onegin", compiled a chain from it, and manually calculated all the statistics.

I thought it would be interesting to do the same thing, 
but not for letters, but for sequences of letters — tokens, and see what the resulting Markov chain can generate.

Here are some interesting and funny examples

```
Не долги дни!

Зато любовь,
Чувства побледней снег навеса

Объемлет,

Он пел победом всё. Татьяне

На грудь
Отворотив игривычное ничего

Последам готов
О скука, там обман!

Ты к ним ходил в нем.

Поскакали ягоду в кустах
```

```
я сердце думала осенью чувственник залётный,

Как много дней

Что я богатеет,
И чем же, Таня? Я, бывало,

А сколько устрицы? пришли! О радостный кладет
На самовару,

А Дуня различны меж собой,

Певец Пиров и суждений,
Хранил Гомера, Фекла и молчит!

Ничто не теперь.

Им наставлен, кто ведал их волненье, свист и пьет за четой.
К минуте мщенья полный лепт, бывало,

Хранила
Первоначальных:
Нашед мой приехав, он почти здоровый,
На стол подвинь я скоро старым бред
```

```
Ее нахал,

И слыша крестящей младостный клад и града,
Фарфор их

Ей строгих тварей минуте мой поэмы Ш. Л. Мальвиной. Так, видя в ней

И, может быть: я сам скучная преждать, подсел

И думал уж невольна:
Я знаю:
```

You can train (set `train = True`) or generate (resp. `train = False`) from `main.py` specifing your text and parameters of tokenizer (`n_gramm`, `sliding`) 

```
user@username:~/.../MarkovChainLM$ main.py
Generating...
100%|██████████████████████████████████████████████████████████████████████████████████████| 39/39 [00:00<00:00, 327.73it/s]
м уборе,
Особенной,
Бывало, почему лукавить.
Приподнялась от друзья и друзей.
Сажают лиц нежне
```

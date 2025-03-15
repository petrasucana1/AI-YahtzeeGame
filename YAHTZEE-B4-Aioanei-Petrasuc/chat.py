
def get_chatbot_response(user_message):
    """Generează un răspuns bazat pe mesajul utilizatorului."""
    user_message = user_message.lower()

    if "reguli" in user_message or "regula" in user_message:
        return (
            "Reguli: Obiectivul jocului YAHTZEE este să obții cât mai multe puncte prin aruncarea a cinci zaruri și realizarea unor combinații specifice de zaruri.\n "
                "Desfășurarea jocului: În fiecare tură, un jucător poate arunca zarurile de până la trei ori. Nu este necesar să arunce toate cele cinci zaruri la a doua și a treia aruncare dintr-o rundă;\n "
                "jucătorul poate pune deoparte câte zaruri dorește și să arunce doar pe cele care nu au numerele pe care încearcă să le obțină.\n "
                "De exemplu, un jucător aruncă zarurile și obține 1, 3, 3, 4, 6. Decide că dorește să încerce să obțină o combinație de „large straight” (1, 2, 3, 4, 5).\n "
                "Așadar, pune deoparte zarurile 1, 3 și 4 și aruncă din nou doar zarurile 3 și 6, sperând să obțină 2 și 5.\n "
                "În acest joc, trebuie să faci clic pe zarurile pe care vrei să le păstrezi. Acestea vor fi mutate în jos și nu vor fi aruncate data viitoare când apeși butonul „Roll Dice”.\n "
                "Dacă decizi, după a doua aruncare dintr-o tură, că nu vrei să păstrezi aceleași zaruri înainte de a treia aruncare, poți face clic din nou pe ele, iar acestea vor fi mutate înapoi pe masă și vor fi aruncate la a treia aruncare.")
    elif "strategie" in user_message or "strategii" in user_message or "strategia" in user_message:
        return (
            "Strategii: \n"
                "- Încearcă să obții bonusul completând secțiunea superioară.\n "
                "Concentrează-te pe aruncări bune cu cinciuri și șesari, astfel încât să nu conteze dacă ai punctaj zero la 1 sau 2.\n"
                "- Poți pune 0 la o combinație dacă nu o ai, chiar dacă ai o altă combinație. De exemplu, dacă ai 2,3,4,5,6 și singurele opțiuni rămase sunt Ones și Sixes, "
                "ar fi mai bine să pui 0 la Ones decât să pui doar 6 la Sixes.\n"
                "- Folosește „Chance” pentru a salva puncte când ai o aruncare slabă.\n\n"
                "Sper să te bucuri de joc!"
        )
    elif "punct" in user_message or "joc" in user_message or "jocuri" in user_message:
        return (
            "- **Ones**: Obține cât mai multe zaruri cu valoarea 1.\n"
            "- **Twos**: Obține cât mai multe zaruri cu valoarea 2.\n"
            "- **Threes**: Obține cât mai multe zaruri cu valoarea 3.\n"
            "- **Fours**: Obține cât mai multe zaruri cu valoarea 4.\n"
            "- **Fives**: Obține cât mai multe zaruri cu valoarea 5.\n"
            "- **Sixes**: Obține cât mai multe zaruri cu valoarea 6.\n"
            "- **Three of a kind**: Obține trei zaruri cu aceeași valoare. Punctele sunt suma tuturor zarurilor (nu doar a celor trei identice).\n"
            "- **Four of a kind**: Obține patru zaruri cu aceeași valoare. Punctele sunt suma tuturor zarurilor (nu doar a celor patru identice).\n"
            "- **Full House**: Obține trei zaruri cu aceeași valoare și o pereche, de exemplu, 1,1,3,3,3 sau 3,3,3,6,6. Valorează 25 de puncte.\n"
            "- **Small Straight**: Obține patru zaruri consecutive, de exemplu, 1,2,3,4 sau 2,3,4,5. Valorează 30 de puncte.\n"
            "- **Large Straight**: Obține cinci zaruri consecutive, de exemplu, 1,2,3,4,5 sau 2,3,4,5,6. Valorează 40 de puncte.\n"
            "- **Chance**: Poți pune orice combinație de zaruri aici. Este practic o soluție de rezervă când nu ai altă opțiune. Scorul este suma zarurilor.\n"
            "- **YAHTZEE**: Obține cinci zaruri identice. Valorează 50 de puncte. Poți obține mai multe Yahtzee-uri, dacă regulile permit."
        )
    elif "ones" in user_message or "Ones" in user_message:
        return "- **Ones**: Obține cât mai multe zaruri cu valoarea 1. Punctajul este suma zarurilor cu valoarea 1."
    elif "twos" in user_message or "Twos" in user_message:
        return "- **Twos**: Obține cât mai multe zaruri cu valoarea 2. Punctajul este suma zarurilor cu valoarea 2."
    elif "threes" in user_message or "Threes" in user_message:
        return "- **Threes**: Obține cât mai multe zaruri cu valoarea 3. Punctajul este suma zarurilor cu valoarea 3."
    elif "fours" in user_message or "Fours" in user_message :
        return "- **Fours**: Obține cât mai multe zaruri cu valoarea 4. Punctajul este suma zarurilor cu valoarea 4."
    elif "fives" in user_message or "Fives" in user_message:
        return "- **Fives**: Obține cât mai multe zaruri cu valoarea 5. Punctajul este suma zarurilor cu valoarea 5."
    elif "sixes" in user_message or "Sixes" in user_message:
        return "- **Sixes**: Obține cât mai multe zaruri cu valoarea 6. Punctajul este suma zarurilor cu valoarea 6."
    elif "three of a kind" in user_message or "Three of a Kind" in user_message :
        return (
            "- **Three of a Kind**: Obține trei zaruri cu aceeași valoare. "
            "Punctajul este suma tuturor zarurilor, nu doar a celor trei identice."
        )
    elif "four of a kind" in user_message or "Four of a Kind" in user_message:
        return (
            "- **Four of a Kind**: Obține patru zaruri cu aceeași valoare. "
            "Punctajul este suma tuturor zarurilor, nu doar a celor patru identice."
        )
    elif "full house" in user_message or "Full Fouse" in user_message:
        return (
            "- **Full House**: Obține trei zaruri cu aceeași valoare și o pereche, "
            "de exemplu, 1,1,3,3,3 sau 3,3,3,6,6. Valorează exact 25 de puncte."
        )
    elif "small straight" in user_message or "Small Straight" in user_message:
        return (
            "- **Small Straight**: Obține patru zaruri consecutive, "
            "de exemplu, 1,2,3,4 sau 2,3,4,5. Valorează exact 30 de puncte."
        )
    elif "large straight" in user_message or "Large Straight" in user_message:
        return (
            "- **Large Straight**: Obține cinci zaruri consecutive, "
            "de exemplu, 1,2,3,4,5 sau 2,3,4,5,6. Valorează exact 40 de puncte."
        )
    elif "chance" in user_message or "Chance" in user_message:
        return (
            "- **Chance**: Poți pune orice combinație de zaruri aici. Este practic o soluție de rezervă când nu ai altă opțiune. "
            "Punctajul este suma tuturor zarurilor."
        )
    elif "yahtzee" in user_message or "Yahtzee" in user_message or "YAHTZEE" in user_message:
        return (
            "- **YAHTZEE**: Obține cinci zaruri identice. Valorează 50 de puncte. "
            "Dacă regulile permit, poți obține puncte suplimentare pentru mai multe Yahtzee-uri."
        )
    else:
        return "Îmi pare rău, nu am înțeles. Poți întreba despre reguli, strategii sau recomandări de mutare."




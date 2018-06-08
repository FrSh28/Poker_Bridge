//Copyright 2018 Yi-Fan Shyu. Some rights reserved.
//CC BY-NC-SA

#include <stdlib.h>
#include <string.h>
#include <sstream>
#include <time.h>
#include <algorithm>
using namespace std;

enum suit {clubs, diamonds, hearts, spades};
suit suits[4] = {clubs, diamonds, hearts, spades};
enum owner {p1, p2, p3, p4, init, throwaway};
const int maxcardnum = 30;
stringstream hss;

//count cardindexnum
inline int cnum(suit i, int j)
{
	return int(i)*13 + j - 1;
}

//singal card
class card{
	suit cardsuit;
	int cardnum;
	owner cardowner;
	
	public:
	card(suit cards, int cardn, owner cardo = init)
	{
		cardsuit = cards;
		cardnum = cardn;
		cardowner = cardo;
	}
	
	suit getsuit()
	{return cardsuit;}
	
	int  getnum()
	{return cardnum;}
	
	owner getowner()
	{return cardowner;}
	
	bool changeowner(owner newcardo)
	{
		cardowner = newcardo;
		return true;
	}
};

//sort card
bool cardsort(card* card1, card* card2)
{
	if(card1->getsuit() > card2->getsuit())
		return true;
	else if(card1->getsuit() == card2->getsuit())
	{
		if(card1->getnum() == 1)
			return true;
		else if(card2->getnum() == 1)
			return false;
		else if(card1->getnum() > card2->getnum())
			return true;
		else
			return false;
	}
	else
		return false;
}

//singal player (see 'init', 'throwaway' as a player)
class player{
	owner playerID;
	char name[50];
	char password[5];
	int cardnum = 0;
	card* playercard[maxcardnum];
	
	public:
	player(owner playernum)
	{
		playerID = playernum;
		strcpy(name, "default");
		strcpy(password, "0000");
	}
	
	owner getID()
	{return playerID;}
	
	char* getname()
	{return name;}
	
	int getcardnum()
	{return cardnum;}
	
	suit getplayercardsuit(int index)
	{return playercard[index]->getsuit();}
	
	int getplayercardnum(int index)
	{return playercard[index]->getnum();}
	
	char* getplayercardinfo(int index)
	{
		if(index > -1 && index < cardnum)
		{
			char cardinfo[10], cardinfonum[5];
			hss<<playercard[index]->getsuit()<<' '<<playercard[index]->getnum();
			hss>>cardinfo;hss>>cardinfonum;
			strcat(cardinfo, " ");
			strcat(cardinfo, cardinfonum);
			hss.str("");hss.clear();
			return cardinfo;
		}
		else
			return NULL;
	}
	
	bool changename(char playername[])
	{
		strcpy(name, playername);
		return true;
	}
	
	bool changepass(char newpass[])
	{
		strcpy(password, newpass);
		return true;
	}
	
	bool checkpass(char check[])
	{
		if(strcmp(password, check))	//equal -> 0
			return false;
		else
			return true;
	}
	
	int findsuitindex(suit check, int num = 0)
	{
		for(int i = num ; i < cardnum ; i++)
			if(playercard[i]->getsuit() == check)
				return i;
		return -1;
	}
	
	card* findsuit(suit check, int num = 0)
	{
		int cardindex = findsuitindex(check, num);
		if(cardindex != -1)
			return playercard[cardindex];
		else
			return NULL;
	}
	
	int findnumindex(int check, int num = 0)
	{
		for(int i = num ; i < cardnum ; i++)
			if(playercard[i]->getnum() == check)
				return i;
		return -1;
	}
	
	card* findnum(int check, int num = 0)
	{
		int cardindex = findnumindex(check, num);
		if(cardindex != -1)
			return playercard[cardindex];
		else
			return NULL;
	}
	
	int findcardindex(card* check, int num = 0)
	{
		for(int i = num ; i < cardnum ; i++)
			if(playercard[i] == check)
				return i;
		return -1;
	}
	
	card* findcard(card* check, int num = 0)
	{
		int cardindex = findcardindex(check, num);
		if(cardindex != -1)
			return playercard[cardindex];
		else
			return NULL;
	}
	
	bool addcard(card* newcard)
	{
		if(cardnum >= 15)
			return false;
		else
		{
			playercard[cardnum] = newcard;
			cardnum++;
			sort(playercard, playercard+cardnum, cardsort);
			return true;
		}
	}
	
	bool throwcard(card* throwncard)
	{
		int cardindex = findcardindex(throwncard);
		if(cardindex != -1)
		{
			playercard[cardindex]->changeowner(throwaway);
			for(int i = cardindex + 1 ; i < cardnum ; i++)
				playercard[i-1] = playercard[i];
			cardnum--;
			return true;
		}
		else
			return false;
	}
};

player* players[4];

//1 poker card
class poker{
	card* cards[52];
	int index[52], drawindex = 51, undraw = 52;
	
	public:
	poker()
	{
		for(int k = 0 ; k < 52 ; k++)
			index[k] = k;
		for(suit i : suits)
			for(int j = 1 ; j <= 13 ; j++)
				cards[cnum(i, j)] = new card(i, j);
	}
	
	~poker()
	{
		for(int i = 0 ; i < 52 ; i++)
			delete cards[i];
	}
	
	card** getallcards()
	{return cards;}
	
	void shuffles()
	{
		for(int i = 0 ; i < 10000 ; i++)
			swap(index[rand()%undraw], index[rand()%undraw]);
	}
	
	card* getcard(suit checksuit, int checknum)
	{
		for(card* i : cards)
			if(i->getsuit() == checksuit && i->getnum() == checknum)
				return i;
		return NULL;
	}
	
	bool drawcard(player* draw)
	{
		if(drawindex>=0 && draw->addcard(cards[index[drawindex]]))
		{
			cards[index[drawindex]]->changeowner(draw->getID());
			drawindex--;
			return true;
		}
		else
			return false;
	}
	
	bool deal(int cardnum)
	{
		for(player* i : players)
			for(int j = 0 ; j < cardnum ; j++)
				if(!drawcard(i))
					return false;
		return true;
	}
};

//init a game
bool initgame(poker** pokercard, player*** play)
{
	srand(time(NULL));
	*pokercard = new poker();
	*play = players;
	(*play)[p1] = new player(p1);
	(*play)[p2] = new player(p2);
	(*play)[p3] = new player(p3);
	(*play)[p4] = new player(p4);
	return true;
}

//terminate a game
bool endgame(poker** pokercard, player*** play)
{
	delete *pokercard;
	delete (*play)[p1];
	delete (*play)[p2];
	delete (*play)[p3];
	delete (*play)[p4];
	return true;
}


//Copyright 2018 Yi-Fan Shyu. Some rights reserved.
//CC BY-NC-SA

#include <iostream>
#include <string.h>
#include <sstream>
#include "poker.h"
#include "communicate.h"
using namespace std;
char PyPath[100] = "C:\\Python27\\python.exe", VpyPath[100] = "";
char Command[200] = "";
stringstream ss;
char mess[20];
bool playagain = true;

bool trywrite(char write[])
{
	if(write_to_client(write))
		return true;
	else
	{
		close();
		cout<<"server error "<<GetLastError()<<endl;
		return false;
	}
}

bool tryread(char read[])
{
	if(read_from_client(read))
		return true;
	else
	{
		close();
		cout<<"client error "<<GetLastError()<<endl;
		return false;
	}
}

bool tryread(char read[], char waiting[])
{
	if(read_from_client(read) && !strcmp(read, waiting))
		return true;
	else
	{
		close();
		cout<<"client error "<<GetLastError()<<endl;
		return false;
	}
}

bool cmpnum(int num1, int num2)//cardnum1>cardnum2 -> True
{
	if(num1 == 1)
		if(num2 != 1)
			return true;
		else
			return false;
	else if(num2 == 1)
			return false;
	else
		return (num1 > num2);
}

int main()
{
	cout<<"Copyright 2018 Yi-Fan Shyu. Some rights reserved.\nCC BY-NC-SA"<<endl;
	//init process
	GetFullPathName("poker_vpy.py", 100, VpyPath, NULL);
	strcat(Command, PyPath);
	strcat(Command, " ");
	strcat(Command, VpyPath);
	while(!create(Command))
	{
		strcpy(Command, "");
		while(GetFileAttributes(PyPath) == INVALID_FILE_ATTRIBUTES)
		{
			char newpath[100] = "";
			cout<<"Can't find Python27 or Python27 module Vpython\n"<<"Path: "<<PyPath<<"\n"
				<<"Change Path?(y/n)"<<endl;
			cin>>newpath;
			if(newpath[0] == 'y' || newpath[0] == 'Y')
			{
				cout<<"Enter the path: ";
				cin>>newpath;
				strcpy(PyPath, newpath);
			}
		}
		while(GetFileAttributes(VpyPath) == INVALID_FILE_ATTRIBUTES)
		{
			char newpath[100] = "";
			cout<<"Can't find Poker_bridge.exe\n"<<"Path: "<<VpyPath<<"\n"
				<<"Change Path?(y/n)"<<endl;
			cin>>newpath;
			if(newpath[0] == 'y' || newpath[0] == 'Y')
			{
				cout<<"Enter the path: ";
				cin>>newpath;
				strcpy(VpyPath, newpath);
			}
		}
		strcat(Command, PyPath);
		strcat(Command, " ");
		strcat(Command, VpyPath);
	}
	char wrbuf[MaxBuf] = "", rdbuf[MaxBuf] = "";
	if(!tryread(rdbuf, "connected"))
		return -1;
	
	HWND hwnd = GetConsoleWindow();
	ShowWindow(hwnd, 6);
	
	poker* gamecard;
	player** gameplayer;
	while(playagain)
	{
		playagain = false;
		//create game
		initgame(&gamecard, &gameplayer);
		gamecard->shuffles();
		gamecard->deal(13);
		owner dealer = p1, nextround;
		int trickrequired = 6, teamtrick[2] = {0, 0};	//[0] p2, p4; [1] p1, p3
		bool notrump = false;
		suit kingsuit;
		
		//set player name & password
		if(!tryread(rdbuf, "setplayer"))
			return -1;
		
		for(int i = 0 ; i < 4 ; i++)
		{
			owner setinfo;
			if(!tryread(rdbuf))
				return -1;
			setinfo = owner(rdbuf[0]-'0');
			
			if(!tryread(rdbuf))
				return -1;
			
			ss<<rdbuf;
			ss>>mess;
			gameplayer[setinfo]->changename(mess);
			ss>>mess;
			gameplayer[setinfo]->changepass(mess);
			ss.str("");ss.clear();
		}
		
		//sent cardinfo to client
		strcpy(wrbuf, "cardinfo");
		if(!trywrite(wrbuf))
			return -1;
		
		for(int i = 0 ; i < 4 ; i++)
		{
			ss<<gameplayer[i]->getID();
			ss>>wrbuf;
			
			if(!trywrite(wrbuf))
				return -1;
			ss.str("");ss.clear();
			
			for(int j = 0 ; j < 13 ; j++)
			{
				strcpy(wrbuf, gameplayer[i]->getplayercardinfo(j));
				if(!trywrite(wrbuf))
					return -1;
				ss.str("");ss.clear();
			}
		}
		
		//call the king
		if(!tryread(rdbuf, "calltheking"))
			return -1;
		
		bool nocall = true, calling = true;
		int playerpass = 0;
		while(calling)
		{
			for(int i = 0 ; i < 4 ; i++)
			{
				if(playerpass >= 3 && !nocall)
				{
					calling = false;
					break;
				}
				owner callinginfo = owner(i);
				
				ss<<callinginfo;
				ss>>wrbuf;
				if(!trywrite(wrbuf))
					return -1;
				ss.str("");ss.clear();
				
				if(!tryread(rdbuf))
					return -1;
				while(!gameplayer[callinginfo]->checkpass(rdbuf))
				{
					strcpy(wrbuf, "False");
					if(!trywrite(wrbuf))
						return -1;
					if(!tryread(rdbuf))
						return -1;
				}
				strcpy(wrbuf, "True");
				if(!trywrite(wrbuf))
					return -1;
				
				if(!tryread(rdbuf))
					return -1;
				ss<<rdbuf;
				ss>>mess;
				
				if(!strcmp(mess, "pass"))
				{
					playerpass++;
					ss.str("");ss.clear();
					continue;
				}
				else
				{
					nocall = false;
					playerpass = 0;
					dealer = callinginfo;
					if((6+int(mess[0]-'0')) > trickrequired)
						trickrequired = (6+int(mess[0]-'0'));
					
					ss>>mess;
					if(!strcmp(mess, "clubs"))
					{
						notrump = false;
						kingsuit = clubs;
					}
					else if(!strcmp(mess, "diamonds"))
					{
						notrump = false;
						kingsuit = diamonds;
					}
					else if(!strcmp(mess, "hearts"))
					{
						notrump = false;
						kingsuit = hearts;
					}
					else if(!strcmp(mess, "spades"))
					{
						notrump = false;
						kingsuit = spades;
					}
					else if(!strcmp(mess, "notrump"))
					{
						notrump = true;
					}
					else
					{
						close();
						cout<<"client error"<<endl;
						return -1;
					}
				}
				ss.str("");ss.clear();
			}
			if(playerpass >= 4 && nocall)
				calling = false;
		}
		if(nocall)
		{
			playagain = true;
			strcpy(wrbuf, "restart");
			if(!trywrite(wrbuf))
				return -1;
			endgame(&gamecard, &gameplayer);
			continue;
		}
		nextround = owner((int(dealer)+1)%4);
		
		//respond
		strcpy(wrbuf, "setOK");
		if(!trywrite(wrbuf))
			return -1;
		
		//play
		if(!tryread(rdbuf, "gaming"))
			return -1;
		
		for(int round = 0 ; round < 13 ; round++)
		{
			owner currentplayer = nextround, roundwinner = currentplayer;
			suit maxsuit, roundsuit;
			int maxnum = 0;
			for(int i = 0 ; i < 4 ; i++)
			{
				ss<<currentplayer;
				ss>>wrbuf;
				if(!trywrite(wrbuf))
					return -1;
				ss.str("");ss.clear();
				if(!tryread(rdbuf))
					return -1;
				while(!gameplayer[currentplayer]->checkpass(rdbuf))
				{
					strcpy(wrbuf, "False");
					if(!trywrite(wrbuf))
						return -1;
					if(!tryread(rdbuf))
						return -1;
				}
				strcpy(wrbuf, "True");
				if(!trywrite(wrbuf))
					return -1;
				
				int cardnum = gameplayer[currentplayer]->getcardnum();
				
				if(i && gameplayer[currentplayer]->findsuitindex(roundsuit) != -1)
				{
					int tempindex = gameplayer[currentplayer]->findsuitindex(roundsuit);
					for(int j = tempindex ; j < cardnum ; j++)
					{
						if(gameplayer[currentplayer]->getplayercardsuit(j) == roundsuit)
						{
							strcpy(wrbuf, gameplayer[currentplayer]->getplayercardinfo(j));
							if(!trywrite(wrbuf))
								return -1;
						}
					}
				}
				else		//first player
				{
					for(int j = 0 ; j < cardnum ; j++)
					{
						strcpy(wrbuf, gameplayer[currentplayer]->getplayercardinfo(j));
						if(!trywrite(wrbuf))
							return -1;
					}
				}
				strcpy(wrbuf, "ends");
				if(!trywrite(wrbuf))
					return -1;
				
				suit playsuit;
				int playnum, suitin;
				if(!tryread(rdbuf))
					return -1;
				ss<<rdbuf;
				ss>>suitin;
				playsuit = suit(suitin);
				ss>>playnum;
				ss.str("");ss.clear();
				if(!i)
				{
					roundsuit = playsuit;
					maxsuit = roundsuit;
					maxnum = playnum;
				}
				gameplayer[currentplayer]->throwcard(gamecard->getcard(playsuit, playnum));
				
				if(notrump)
				{
					if(cmpnum(playnum, maxnum))
					{
						roundwinner = currentplayer;
						maxsuit = playsuit;
						maxnum = playnum;
					}
				}
				else if(playsuit == kingsuit)
				{
					if(maxsuit == kingsuit)
					{
						if(cmpnum(playnum, maxnum))
						{
							roundwinner = currentplayer;
							maxsuit = playsuit;
							maxnum = playnum;
						}
					}
					else
					{
						roundwinner = currentplayer;
						maxsuit = playsuit;
						maxnum = playnum;
					}
				}
				else
				{
					if(playsuit == maxsuit && cmpnum(playnum, maxnum))
					{
						roundwinner = currentplayer;
						maxsuit = playsuit;
						maxnum = playnum;
					}
				}
				currentplayer = owner((int(currentplayer)+1)%4);
			}
			teamtrick[(roundwinner & 1)]++;
			nextround = roundwinner;
			ss<<roundwinner;
			ss>>wrbuf;
			if(!trywrite(wrbuf))
				return -1;
			ss.str("");ss.clear();
		}
		
		//calculate score
		strcpy(wrbuf, "score");
		if(!trywrite(wrbuf))
			return -1;
		
		if(teamtrick[(dealer & 1)] >= trickrequired)
		{
			ss<<(dealer & 1);
			ss>>wrbuf;
			if(!trywrite(wrbuf))
				return -1;
			ss.str("");ss.clear();
		}
		else
		{
			ss<<!(dealer & 1);
			ss>>wrbuf;
			if(!trywrite(wrbuf))
				return -1;
			ss.str("");ss.clear();
		}
		
		ss<<(dealer & 1)<<' '<<teamtrick[(dealer & 1)];
		ss>>mess;
		strcpy(wrbuf, mess);
		ss>>mess;
		strcat(wrbuf, " ");
		strcat(wrbuf, mess);
		if(!trywrite(wrbuf))
			return -1;
		ss.str("");ss.clear();
		
		ss<<(!(dealer & 1))<<' '<<teamtrick[!(dealer & 1)];
		ss>>mess;
		strcpy(wrbuf, mess);
		ss>>mess;
		strcat(wrbuf, " ");
		strcat(wrbuf, mess);
		if(!trywrite(wrbuf))
			return -1;
		ss.str("");ss.clear();
		
		//terminate game
		endgame(&gamecard, &gameplayer);
		
		//play again?
		if(!tryread(rdbuf))
			return -1;
		if(!strcmp(rdbuf, "playagain"))
			playagain = true;
	}
	
	close();
	return 0;
}

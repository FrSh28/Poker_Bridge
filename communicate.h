//Copyright 2018 Yi-Fan Shyu. Some rights reserved.
//CC BY-NC-SA

#include <string.h>
#include <windows.h>
#include <iostream>
using namespace std;
#define output "\\\\.\\pipe\\pokerbridge_wr"	//"\\.\pipe\pokerbridge_wr"
#define input "\\\\.\\pipe\\pokerbridge_rd"	//"\\.\pipe\pokerbridge_rd"
#define MaxBuf 50
HANDLE wr = NULL, rd = NULL;
const int timeout = 2;
STARTUPINFO si;
PROCESS_INFORMATION pi;
void close(bool ClientStart = true);

bool create(char ClientCommand[])
{
	//create named pipe
	wr = CreateNamedPipe(output, PIPE_ACCESS_OUTBOUND,
					PIPE_WAIT|PIPE_TYPE_MESSAGE|PIPE_READMODE_MESSAGE|PIPE_REJECT_REMOTE_CLIENTS,
					1, MaxBuf, MaxBuf, 0, NULL);
	rd = CreateNamedPipe(input, PIPE_ACCESS_INBOUND,
					PIPE_WAIT|PIPE_TYPE_MESSAGE|PIPE_READMODE_MESSAGE|PIPE_REJECT_REMOTE_CLIENTS,
					1, MaxBuf, MaxBuf, 0, NULL);
	if(wr == INVALID_HANDLE_VALUE && rd == INVALID_HANDLE_VALUE)
		return false;
	
	//execute client
	ZeroMemory(&si, sizeof(si));
	si.cb = sizeof(si);
	ZeroMemory(&pi, sizeof(pi));
	if(!CreateProcess(NULL, ClientCommand, NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi))
	{
		close(false);
		return false;
	}
	
	//connect to client
	if(!ConnectNamedPipe(wr, NULL) && GetLastError() != ERROR_PIPE_CONNECTED)
		close();
	if(!ConnectNamedPipe(rd, NULL) && GetLastError() != ERROR_PIPE_CONNECTED)
		close();
	
	return true;
}

bool write_to_client(char message[])
{
	DWORD wrlen = 0;
	FlushFileBuffers(wr);
	int times = 0;
	while(times < timeout)
	{
		if(WriteFile(wr, message, MaxBuf, &wrlen, 0))
			return true;
		times++;
	}
	return false;
}
	
bool read_from_client(char message[])
{
	DWORD rdlen = 0;
	int times = 0;
	while(times < timeout)
	{
		if(ReadFile(rd, message, MaxBuf, &rdlen, 0))
			return true;
		times++;
	}
	return false;
}

void close(bool ClientStart)
{
	FlushFileBuffers(wr);
	//close pipe
	DisconnectNamedPipe(wr);
	CloseHandle(wr);
	DisconnectNamedPipe(rd);
	CloseHandle(rd);
	//ends client
	if(ClientStart)
	{
		WaitForSingleObject(pi.hProcess, INFINITE);
		CloseHandle(pi.hProcess);
		CloseHandle(pi.hThread);
	}
}

void reconnect()
{
	DisconnectNamedPipe(wr);
	DisconnectNamedPipe(rd);
	if(!ConnectNamedPipe(wr, NULL) && GetLastError() != ERROR_PIPE_CONNECTED)
		close();
	if(!ConnectNamedPipe(rd, NULL) && GetLastError() != ERROR_PIPE_CONNECTED)
		close();
}

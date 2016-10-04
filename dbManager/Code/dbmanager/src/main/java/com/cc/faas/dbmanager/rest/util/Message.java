package com.cc.faas.dbmanager.rest.util;

public class Message {
private String errorMessage;

public Message(){
	
}
public Message(String errorMessage){
	this.errorMessage=errorMessage;
}

public String getErrorMessage() {
	return errorMessage;
}

public void setErrorMessage(String errorMessage) {
	this.errorMessage = errorMessage;
}

}

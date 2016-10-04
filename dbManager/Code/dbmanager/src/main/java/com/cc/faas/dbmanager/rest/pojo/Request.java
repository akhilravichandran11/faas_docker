package com.cc.faas.dbmanager.rest.pojo;

import javax.xml.bind.annotation.XmlRootElement;

@XmlRootElement(name="request")
public class Request {
	private String requestId;
	private String requestType;
	private String requestStatus;
	private String requestParameters;
	private String result;
	private User requestor;
	public String getRequestId() {
		return requestId;
	}
	public void setRequestId(String requestId) {
		this.requestId = requestId;
	}
	public String getRequestType() {
		return requestType;
	}
	public void setRequestType(String requestType) {
		this.requestType = requestType;
	}
	public String getRequestParameters() {
		return requestParameters;
	}
	public void setRequestParameters(String requestParameters) {
		this.requestParameters = requestParameters;
	}
	public String getResult() {
		return result;
	}
	public void setResult(String result) {
		this.result = result;
	}
	public User getRequestor() {
		return requestor;
	}
	public void setRequestor(User requestor) {
		this.requestor = requestor;
	}
	public String getRequestStatus() {
		return requestStatus;
	}
	public void setRequestStatus(String requestStatus) {
		this.requestStatus = requestStatus;
	}

}

package com.cc.faas.dbmanager.rest.pojo;

import javax.xml.bind.annotation.XmlRootElement;

@XmlRootElement(name="function")
public class Function {
	private String functionId;
	private String functionName;
	private String functionContent;
	private User creator;
	public String getFunctionId() {
		return functionId;
	}
	public void setFunctionId(String functionId) {
		this.functionId = functionId;
	}
	public String getFunctionName() {
		return functionName;
	}
	public void setFunctionName(String functionName) {
		this.functionName = functionName;
	}
	public String getFunctionContent() {
		return functionContent;
	}
	public void setFunctionContent(String functionContent) {
		this.functionContent = functionContent;
	}
	public User getCreator() {
		return creator;
	}
	public void setCreator(User creator) {
		this.creator = creator;
	}

}

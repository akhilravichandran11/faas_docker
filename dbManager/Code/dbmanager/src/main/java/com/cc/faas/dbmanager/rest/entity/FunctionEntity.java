package com.cc.faas.dbmanager.rest.entity;

import java.io.Serializable;

import javax.persistence.Access;
import javax.persistence.AccessType;
import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import org.hibernate.annotations.Fetch;
import org.hibernate.annotations.FetchMode;

@Entity
@Table(name = "function", catalog = "faas",schema="public")
@Access(AccessType.PROPERTY)
public class FunctionEntity implements Serializable {

private static final long serialVersionUID = 7079891000021328079L;
private String id;
private String name;
private String content;
private UserEntity user;

@Id
@Column(name = "id")
public String getId() {
	return id;
}

public void setId(String id) {
	this.id = id;
}

@Column(name = "name")
public String getName() {
	return name;
}
public void setName(String name) {
	this.name = name;
}

@Column(name = "content")
public String getContent() {
	return content;
}
public void setContent(String content) {
	this.content = content;
}
@ManyToOne(fetch = FetchType.EAGER, cascade = CascadeType.PERSIST)
@JoinColumn(name = "userid", referencedColumnName="id")
@Fetch(FetchMode.SELECT)
public UserEntity getUser() {
	return user;
}
public void setUser(UserEntity user) {
	this.user = user;
}

}

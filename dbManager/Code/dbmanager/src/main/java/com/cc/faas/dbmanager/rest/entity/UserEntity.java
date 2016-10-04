package com.cc.faas.dbmanager.rest.entity;

import java.io.Serializable;
import java.util.List;

import javax.persistence.Access;
import javax.persistence.AccessType;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.Id;
import javax.persistence.OneToMany;
import javax.persistence.Table;

import org.hibernate.annotations.Fetch;
import org.hibernate.annotations.FetchMode;
import org.hibernate.annotations.NotFound;
import org.hibernate.annotations.NotFoundAction;

@Entity
@Table(name = "reguser", catalog = "faas",schema="public")
@Access(AccessType.PROPERTY)
public class UserEntity implements Serializable{
private static final long serialVersionUID = -2021275495411017185L;


private String id;
private String name;
private String password;
private List<FunctionEntity>functions;
private List<RequestEntity>requests;

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

@Column(name = "password")
public String getPassword() {
	return password;
}
public void setPassword(String password) {
	this.password = password;
}
@org.hibernate.annotations.BatchSize(size = 5)
@OneToMany(mappedBy = "user", fetch = FetchType.LAZY)
@NotFound(action = NotFoundAction.IGNORE)
@Fetch(FetchMode.SELECT)
public List<FunctionEntity> getFunctions() {
	return functions;
}
public void setFunctions(List<FunctionEntity> functions) {
	this.functions = functions;
}

@org.hibernate.annotations.BatchSize(size = 5)
@OneToMany(mappedBy = "user", fetch = FetchType.LAZY)
@NotFound(action = NotFoundAction.IGNORE)
@Fetch(FetchMode.SELECT)
public List<RequestEntity> getRequests() {
	return requests;
}
public void setRequests(List<RequestEntity> requests) {
	this.requests = requests;
}

}

package com.cc.faas.dbmanager.rest.service;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.UUID;

import com.cc.faas.dbmanager.rest.constants.ExceptionConstants;
import com.cc.faas.dbmanager.rest.dao.UserDaoImpl;
import com.cc.faas.dbmanager.rest.entity.UserEntity;
import com.cc.faas.dbmanager.rest.pojo.User;

public class UserServiceImpl {
	private UserDaoImpl userDao = new UserDaoImpl();

	public User createUser(User userToCreate) throws Exception {
		UserEntity entityInDb=userDao.findByName(userToCreate.getUserName());
		if(entityInDb != null){
			throw new Exception(ExceptionConstants.NAME_IN_DB);
		}
		UserEntity userEntity = fromDto(userToCreate);
		userDao.createUser(userEntity);
		return toDto(userDao.findById(userEntity.getId()));
	}
	public User updateUser(User userToUpdate) throws Exception {
		UserEntity entityInDb=userDao.findById(userToUpdate.getUserId());
		if(entityInDb==null){
			throw new Exception(ExceptionConstants.ID_NOT_IN_DB);
		}
		UserEntity userEntity = fromDto(userToUpdate);
		userDao.updateUser(userEntity);
		return toDto(userDao.findById(userEntity.getId()));
	}
	public void deleteUser(String id) throws Exception {
		UserEntity entityInDb=userDao.findById(id);
		if(entityInDb==null){
			throw new Exception(ExceptionConstants.ID_NOT_IN_DB);
		}
		userDao.deleteUser(id);
	}
	public User getUserById(String id) throws Exception {
		UserEntity entityInDb=userDao.findById(id);
		if(entityInDb == null){
			return null;
		}else{

			return toDto(entityInDb);
		}
	}
	public User getUserByName(String name) throws Exception {
		UserEntity entityInDb=userDao.findByName(name);
		if(entityInDb == null){
			return null;
		}else{

			return toDto(entityInDb);
		}
	}
	public List<User> getUsers() throws Exception {
		List<User>users=new ArrayList<User>();
		List<UserEntity> entities=userDao.getAll();
		if(entities != null && !entities.isEmpty()){
			for(UserEntity entity: entities){
				users.add(toDto(entity));
			}
		}
		return users;
	}
	public void authenticateUser(User userToAuthenticate) throws Exception {
		UserEntity entityInDb=userDao.findByName(userToAuthenticate.getUserName());
		if(entityInDb == null){
			throw new Exception(ExceptionConstants.ID_NOT_IN_DB);
		}
		if(entityInDb.getPassword().equals(userToAuthenticate.getPassword())){
			throw new Exception(ExceptionConstants.ID_NOT_IN_DB);
		}
	}
	public static UserEntity fromDto(User user) {
		UserEntity entity = new UserEntity();
		if(user.getUserId()!=null && !user.getUserId().isEmpty()){
			entity.setId(user.getUserId());
		}else{
			entity.setId(UUID.randomUUID().toString().toUpperCase(Locale.US));
		}
		entity.setName(user.getUserName());
		entity.setPassword(user.getPassword());
		return entity;
	}
	public static User toDto(UserEntity entity){
		User user = new User();
		user.setUserId(entity.getId());
		user.setUserName(entity.getName());
		return user;
	}
}
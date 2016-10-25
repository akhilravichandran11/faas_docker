package com.cc.faas.dbmanager.rest.service;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.UUID;

import com.cc.faas.dbmanager.rest.constants.ExceptionConstants;
import com.cc.faas.dbmanager.rest.dao.FunctionDaoImpl;
import com.cc.faas.dbmanager.rest.dao.UserDaoImpl;
import com.cc.faas.dbmanager.rest.entity.FunctionEntity;
import com.cc.faas.dbmanager.rest.entity.UserEntity;
import com.cc.faas.dbmanager.rest.pojo.Function;
import com.cc.faas.dbmanager.rest.pojo.User;

public class FunctionServiceImpl {
	private FunctionDaoImpl functionDao = new FunctionDaoImpl();
	private UserDaoImpl userDao = new UserDaoImpl();

	public Function createFunction(Function functionToCreate) throws Exception {
		UserEntity creator = userDao.findById(functionToCreate.getCreator().getUserId());
		if(creator==null){
			throw new Exception(ExceptionConstants.ID_NOT_IN_DB);
		}
		FunctionEntity entityInDb = functionDao.findByNameAndUserId(creator.getId(), functionToCreate.getFunctionName());
		if(entityInDb!=null){
			throw new Exception(ExceptionConstants.NAME_IN_DB);
		}
		FunctionEntity functionEntity = fromDto(functionToCreate,creator);
		functionDao.createFunction(functionEntity);
		return toDto(functionDao.findById(functionEntity.getId()));
	}
	public Function updateFunction(Function functionToUpdate) throws Exception {
		FunctionEntity entityInDb=functionDao.findById(functionToUpdate.getFunctionId());
		if(entityInDb==null){
			throw new Exception(ExceptionConstants.ID_NOT_IN_DB);
		}
		UserEntity creator = userDao.findById(functionToUpdate.getCreator().getUserId());
		if(creator==null){
			throw new Exception(ExceptionConstants.ID_NOT_IN_DB);
		}
		FunctionEntity functionEntity = fromDto(functionToUpdate,creator);
		functionDao.updateFunction(functionEntity);
		return toDto(functionDao.findById(functionEntity.getId()));
	}
	public void deleteFunction(String id) throws Exception {
		FunctionEntity entityInDb=functionDao.findById(id);
		if(entityInDb==null){
			throw new Exception(ExceptionConstants.ID_NOT_IN_DB);
		}
		functionDao.deleteFunction(id);
	}
	public Function getFunctionById(String id) throws Exception {
		FunctionEntity entityInDb=functionDao.findById(id);
		if(entityInDb == null){
			return null;
		}else{

			return toDto(entityInDb);
		}
	}

	public List<Function> getFunctions() throws Exception {
		List<Function>functions=new ArrayList<Function>();
		List<FunctionEntity> entities=functionDao.getAll();
		if(entities != null && !entities.isEmpty()){
			for(FunctionEntity entity: entities){
				functions.add(toDto(entity));
			}
		}
		return functions;
	}
	public static FunctionEntity fromDto(Function function, UserEntity creator) {
		FunctionEntity entity = new FunctionEntity();
		if(function.getFunctionId() !=null && !function.getFunctionId().isEmpty()){
			entity.setId(function.getFunctionId());
		}else{
			entity.setId(UUID.randomUUID().toString().toUpperCase(Locale.US));
		}
		entity.setName(function.getFunctionName());
		entity.setContent(function.getFunctionContent());
		entity.setUser(creator);
		return entity;
	}
	public static Function toDto(FunctionEntity entity){
		Function function = new Function();
		User creator = UserServiceImpl.toDto(entity.getUser());
		function.setFunctionId(entity.getId());
		function.setFunctionName(entity.getName());
		function.setFunctionContent(entity.getContent());
		function.setCreator(creator);
		return function;
	}
}
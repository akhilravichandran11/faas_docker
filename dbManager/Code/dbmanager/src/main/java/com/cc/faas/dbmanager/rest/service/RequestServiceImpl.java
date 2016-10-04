package com.cc.faas.dbmanager.rest.service;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.UUID;

import com.cc.faas.dbmanager.rest.constants.ExceptionConstants;
import com.cc.faas.dbmanager.rest.dao.RequestDaoImpl;
import com.cc.faas.dbmanager.rest.dao.UserDaoImpl;
import com.cc.faas.dbmanager.rest.entity.RequestEntity;
import com.cc.faas.dbmanager.rest.entity.UserEntity;
import com.cc.faas.dbmanager.rest.pojo.Request;
import com.cc.faas.dbmanager.rest.pojo.User;

public class RequestServiceImpl {
	private RequestDaoImpl requestDao = new RequestDaoImpl();
	private UserDaoImpl userDao = new UserDaoImpl();

	public Request createRequest(Request requestToCreate) throws Exception {
		UserEntity requestor = userDao.findById(requestToCreate.getRequestor().getUserId());
		if(requestor==null){
			throw new Exception(ExceptionConstants.ID_NOT_IN_DB);
		}
		RequestEntity requestEntity = fromDto(requestToCreate,requestor);
		requestDao.createRequest(requestEntity);
		return toDto(requestDao.findById(requestEntity.getId()));
	}
	public Request updateRequest(Request requestToUpdate) throws Exception {
		RequestEntity entityInDb=requestDao.findById(requestToUpdate.getRequestId());
		if(entityInDb==null){
			throw new Exception(ExceptionConstants.ID_NOT_IN_DB);
		}
		UserEntity requestor = userDao.findById(requestToUpdate.getRequestor().getUserId());
		if(requestor==null){
			throw new Exception(ExceptionConstants.ID_NOT_IN_DB);
		}
		RequestEntity requestEntity = fromDto(requestToUpdate,requestor);
		requestDao.updateRequest(requestEntity);
		return toDto(requestDao.findById(requestEntity.getId()));
	}
	public void deleteFunction(String id) throws Exception {
		RequestEntity entityInDb=requestDao.findById(id);
		if(entityInDb==null){
			throw new Exception(ExceptionConstants.ID_NOT_IN_DB);
		}
		requestDao.deleteRequest(id);
	}
	public Request getRequestById(String id) throws Exception {
		RequestEntity entityInDb=requestDao.findById(id);
		if(entityInDb == null){
			return null;
		}else{

			return toDto(entityInDb);
		}
	}

	public List<Request> getRequests() throws Exception {
		List<Request>functions=new ArrayList<Request>();
		List<RequestEntity> entities=requestDao.getAll();
		if(entities != null && !entities.isEmpty()){
			for(RequestEntity entity: entities){
				functions.add(toDto(entity));
			}
		}
		return functions;
	}
	public static RequestEntity fromDto(Request request, UserEntity requestor) {
		RequestEntity entity = new RequestEntity();
		if(request.getRequestId() !=null && !request.getRequestId().isEmpty()){
			entity.setId(request.getRequestId());
		}else{
			entity.setId(UUID.randomUUID().toString().toUpperCase(Locale.US));
		}
		entity.setParameter(request.getRequestParameters());
		entity.setResult(request.getResult());
		entity.setStatus(request.getRequestStatus());
		entity.setType(request.getRequestType());
		entity.setUser(requestor);
		return entity;
	}
	public static Request toDto(RequestEntity entity){
		Request request = new Request();
		User requestor = UserServiceImpl.toDto(entity.getUser());
		request.setRequestId(entity.getId());
		request.setRequestor(requestor);
		request.setRequestParameters(entity.getParameter());
		request.setRequestStatus(entity.getStatus());
		request.setRequestType(entity.getType());
		request.setResult(entity.getResult());
		return request;
	}
}

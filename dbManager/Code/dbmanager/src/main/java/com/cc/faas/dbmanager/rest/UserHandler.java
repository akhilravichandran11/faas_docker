package com.cc.faas.dbmanager.rest;

import java.util.List;

import javax.ws.rs.Consumes;
import javax.ws.rs.DELETE;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.PUT;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import javax.ws.rs.core.Response.Status;

import com.cc.faas.dbmanager.rest.constants.ExceptionConstants;
import com.cc.faas.dbmanager.rest.pojo.User;
import com.cc.faas.dbmanager.rest.service.UserServiceImpl;
import com.cc.faas.dbmanager.rest.util.Helper;
import com.cc.faas.dbmanager.rest.util.Message;

@Path("/users")
public class UserHandler {

	private UserServiceImpl userService = new UserServiceImpl();

	@GET
	@Path("/{username}")
	public Response getUser(@PathParam("username") String name) {
		User requestedUser=null;
		try
		{
			requestedUser=userService.getUserByName(name);
		} catch (Exception e) {
			return Response.status(Status.INTERNAL_SERVER_ERROR).entity(Helper.convertToJsonString(new Message(e.getMessage()))).build();
		}
		if(requestedUser==null){
			return Response.status(Status.NOT_FOUND).entity(Helper.convertToJsonString(new Message(ExceptionConstants.NAME_NOT_EXIST))).build();
		}else{
			return Response.status(Status.OK).entity(Helper.convertToJsonString(requestedUser)).build();
		}
	}
	@GET
	@Path("/id/{userid}")
	public Response getUserById(@PathParam("userid") String id) {

		User requestedUser=null;
		try
		{
			requestedUser=userService.getUserById(id);
		} catch (Exception e) {
			return Response.status(Status.INTERNAL_SERVER_ERROR).entity(Helper.convertToJsonString(new Message(e.getMessage()))).build();
		}
		if(requestedUser==null){
			return Response.status(Status.NOT_FOUND).entity(Helper.convertToJsonString(new Message(ExceptionConstants.ID_NOT_EXIST))).build();
		}else{
			return Response.status(Status.OK).entity(Helper.convertToJsonString(requestedUser)).build();
		}

	}

	@GET
	public Response getAllUsers() {

		List<User> users;
		try {
			users=userService.getUsers();
		} catch (Exception e) {
			return Response.status(Status.INTERNAL_SERVER_ERROR).entity(Helper.convertToJsonString(new Message(e.getMessage()))).build();
		}
		return Response.status(Status.OK).entity(Helper.convertToJsonString(users)).build();
	}

	@POST
	@Consumes(MediaType.APPLICATION_JSON)
	public Response createUser(User user) {
		if(user==null||user.getUserName()==null || user.getUserName().isEmpty() || user.getPassword()==null || user.getPassword().isEmpty()){
			return Response.status(Status.BAD_REQUEST).entity(Helper.convertToJsonString(new Message(ExceptionConstants.NULL_EMPTY_INPUT))).build();
		}
		try{
			User createdUser=userService.createUser(user);
			return Response.status(Status.CREATED).entity(Helper.convertToJsonString(createdUser)).build();
		}catch(Exception ex){
			if(Helper.checkBadRequest(ex)){
				return Response.status(Status.BAD_REQUEST).entity(Helper.convertToJsonString(new Message(ex.getMessage() + "Dude 1"))).build();
			}
			return Response.status(Status.INTERNAL_SERVER_ERROR).entity(Helper.convertToJsonString(new Message(ex.getMessage() + "Dude 2"))).build();
		}
	}
	@PUT
	@Consumes(MediaType.APPLICATION_JSON)
	public Response updateUser(User user) {
		if(user==null||user.getUserId()==null || user.getUserId().isEmpty() || user.getUserName()==null || user.getUserName().isEmpty() || user.getPassword()==null || user.getPassword().isEmpty()){
			return Response.status(Status.BAD_REQUEST).entity(Helper.convertToJsonString(new Message(ExceptionConstants.NULL_EMPTY_INPUT))).build();
		}
		try{
			User updatedUser=userService.updateUser(user);
			return Response.status(Status.OK).entity(Helper.convertToJsonString(updatedUser)).build();
		}catch(Exception ex){
			if(Helper.checkBadRequest(ex)){
				return Response.status(Status.BAD_REQUEST).entity(Helper.convertToJsonString(new Message(ex.getMessage()))).build();
			}
			return Response.status(Status.INTERNAL_SERVER_ERROR).entity(Helper.convertToJsonString(new Message(ex.getMessage()))).build();
		}
	}
	@DELETE
	@Path("/{userid}")
	public Response deleteUser(@PathParam("userid") String id) {
		try{
			userService.deleteUser(id);
			return Response.status(Status.NO_CONTENT).build();
		}catch(Exception ex){
			return Response.status(Status.INTERNAL_SERVER_ERROR).entity(Helper.convertToJsonString(new Message(ex.getMessage()))).build();
		}
	}
	@POST
	@Path("/auth")
	@Consumes(MediaType.APPLICATION_JSON)
	public Response authenticateUser(User user) {
		if(user==null||user.getUserName()==null || user.getUserName().isEmpty() || user.getPassword()==null || user.getPassword().isEmpty()){
			return Response.status(Status.BAD_REQUEST).entity(Helper.convertToJsonString(new Message(ExceptionConstants.INVALID_CREDENTIALS))).build();
		}
		try{
			userService.authenticateUser(user);
			return Response.status(Status.NO_CONTENT).build();
		}catch(Exception ex){
			if(Helper.checkBadRequest(ex)){
				return Response.status(Status.BAD_REQUEST).entity(Helper.convertToJsonString(new Message(ExceptionConstants.INVALID_CREDENTIALS))).build();
			}
			return Response.status(Status.INTERNAL_SERVER_ERROR).entity(Helper.convertToJsonString(new Message(ex.getMessage()))).build();
		}
	}
}
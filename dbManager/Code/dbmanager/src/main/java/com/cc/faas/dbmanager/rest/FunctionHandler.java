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
import com.cc.faas.dbmanager.rest.pojo.Function;
import com.cc.faas.dbmanager.rest.service.FunctionServiceImpl;
import com.cc.faas.dbmanager.rest.util.Helper;
import com.cc.faas.dbmanager.rest.util.Message;

@Path("/functions")
public class FunctionHandler {
	private FunctionServiceImpl functionService = new FunctionServiceImpl();
	@GET
	@Path("/{id}")
	public Response getFunctionById(@PathParam("id") String id) {

		Function requestedFunction=null;
		try
		{
			requestedFunction=functionService.getFunctionById(id);
		} catch (Exception e) {
			return Response.status(Status.INTERNAL_SERVER_ERROR).entity(Helper.convertToJsonString(new Message(e.getMessage()))).build();
		}
		if(requestedFunction==null){
			return Response.status(Status.NOT_FOUND).entity(Helper.convertToJsonString(new Message(ExceptionConstants.ID_NOT_EXIST))).build();
		}else{
			return Response.status(Status.OK).entity(Helper.convertToJsonString(requestedFunction)).build();
		}
	}
	
	@GET
	public Response getAllFunctions() {
		List<Function> functions;
		try {
			functions=functionService.getFunctions();
		} catch (Exception e) {
			return Response.status(Status.INTERNAL_SERVER_ERROR).entity(Helper.convertToJsonString(new Message(e.getMessage()))).build();
		}
		return Response.status(Status.OK).entity(Helper.convertToJsonString(functions)).build();

	}

	@POST
	@Consumes(MediaType.APPLICATION_JSON)
	public Response createFunction(Function function) {
		if(function==null||function.getFunctionName()==null||function.getFunctionName().isEmpty()||function.getFunctionContent()==null||function.getFunctionContent().isEmpty()||function.getCreator()==null||function.getCreator().getUserId()==null||function.getCreator().getUserId().isEmpty()){
			return Response.status(Status.BAD_REQUEST).entity(Helper.convertToJsonString(new Message(ExceptionConstants.NULL_EMPTY_INPUT))).build();
		}
		try{
			Function createdFunction=functionService.createFunction(function);
			return Response.status(Status.CREATED).entity(Helper.convertToJsonString(createdFunction)).build();
		}catch(Exception ex){
			if(Helper.checkBadRequest(ex)){
				return Response.status(Status.BAD_REQUEST).entity(Helper.convertToJsonString(new Message(ex.getMessage()))).build();
			}
			return Response.status(Status.INTERNAL_SERVER_ERROR).entity(Helper.convertToJsonString(new Message(ex.getMessage()))).build();
		}
	}
	@PUT
	@Consumes(MediaType.APPLICATION_JSON)
	public Response updateFunction(Function function) {
		if(function==null||function.getFunctionId()==null||function.getFunctionId().isEmpty()||function.getFunctionName()==null||function.getFunctionName().isEmpty()||function.getFunctionContent()==null||function.getFunctionContent().isEmpty()||function.getCreator()==null||function.getCreator().getUserId()==null||function.getCreator().getUserId().isEmpty()){
			return Response.status(Status.BAD_REQUEST).entity(Helper.convertToJsonString(new Message(ExceptionConstants.NULL_EMPTY_INPUT))).build();
		}
		try{
			Function updatedFunction=functionService.updateFunction(function);
			return Response.status(Status.OK).entity(Helper.convertToJsonString(updatedFunction)).build();
		}catch(Exception ex){
			if(Helper.checkBadRequest(ex)){
				return Response.status(Status.BAD_REQUEST).entity(Helper.convertToJsonString(new Message(ex.getMessage()))).build();
			}
			return Response.status(Status.INTERNAL_SERVER_ERROR).entity(Helper.convertToJsonString(new Message(ex.getMessage()))).build();
		}
	}
	@DELETE
	@Path("/{functionId}")
	public Response deleteFunction(@PathParam("functionId") String id) {
		try{
			functionService.deleteFunction(id);
			return Response.status(Status.NO_CONTENT).build();
		}catch(Exception ex){
			return Response.status(Status.INTERNAL_SERVER_ERROR).entity(Helper.convertToJsonString(new Message(ex.getMessage()))).build();
		}
	}
}

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
import com.cc.faas.dbmanager.rest.pojo.Request;
import com.cc.faas.dbmanager.rest.service.RequestServiceImpl;
import com.cc.faas.dbmanager.rest.util.Helper;
import com.cc.faas.dbmanager.rest.util.Message;

@Path("/request")
public class RequestHandler {
	private RequestServiceImpl requestService= new RequestServiceImpl();
	
	@GET
	@Path("/{id}")
	public Response getRequest(@PathParam("id") String id) {

		Request request=null;
		try
		{
			request=requestService.getRequestById(id);
		} catch (Exception e) {
			return Response.status(Status.INTERNAL_SERVER_ERROR).entity(Helper.convertToJsonString(new Message(e.getMessage()))).build();
		}
		if(request==null){
			return Response.status(Status.NOT_FOUND).entity(Helper.convertToJsonString(new Message(ExceptionConstants.ID_NOT_EXIST))).build();
		}else{
			return Response.status(Status.OK).entity(Helper.convertToJsonString(request)).build();
		}

	}
	
	@GET
	public Response getAllRequests() {
		List<Request> requests;
		try {
			requests=requestService.getRequests();
		} catch (Exception e) {
			return Response.status(Status.INTERNAL_SERVER_ERROR).entity(Helper.convertToJsonString(new Message(e.getMessage()))).build();
		}
		return Response.status(Status.OK).entity(Helper.convertToJsonString(requests)).build();

	}

	@POST
	@Consumes(MediaType.APPLICATION_JSON)
	public Response createRequest(Request request) {
		if(request==null||request.getRequestor()==null||request.getRequestor().getUserId()==null||request.getRequestor().getUserId().isEmpty()||request.getRequestType()==null||request.getRequestType().isEmpty()){
			return Response.status(Status.BAD_REQUEST).entity(Helper.convertToJsonString(new Message(ExceptionConstants.NULL_EMPTY_INPUT))).build();
		}
		try{
			Request createdRequest=requestService.createRequest(request);
			return Response.status(Status.CREATED).entity(Helper.convertToJsonString(createdRequest)).build();
		}catch(Exception ex){
			if(Helper.checkBadRequest(ex)){
				return Response.status(Status.BAD_REQUEST).entity(Helper.convertToJsonString(new Message(ex.getMessage()))).build();
			}
			return Response.status(Status.INTERNAL_SERVER_ERROR).entity(Helper.convertToJsonString(new Message(ex.getMessage()))).build();
		}
	}
	@PUT
	@Consumes(MediaType.APPLICATION_JSON)
	public Response updateRequest(Request request) {
		if(request==null||request.getRequestId()==null||request.getRequestId().isEmpty()||request.getRequestor()==null||request.getRequestor().getUserId()==null||request.getRequestor().getUserId().isEmpty()||request.getRequestType()==null||request.getRequestType().isEmpty()){
			return Response.status(Status.BAD_REQUEST).entity(Helper.convertToJsonString(new Message(ExceptionConstants.NULL_EMPTY_INPUT))).build();
		}
		try{
			Request updatedRequest=requestService.updateRequest(request);
			return Response.status(Status.OK).entity(Helper.convertToJsonString(updatedRequest)).build();
		}catch(Exception ex){
			if(Helper.checkBadRequest(ex)){
				return Response.status(Status.BAD_REQUEST).entity(Helper.convertToJsonString(new Message(ex.getMessage()))).build();
			}
			return Response.status(Status.INTERNAL_SERVER_ERROR).entity(Helper.convertToJsonString(new Message(ex.getMessage()))).build();
		}
	}
	@DELETE
	@Path("/{requestId}")
	public Response deleteRequest(@PathParam("requestId") String id) {
		try{
			requestService.deleteFunction(id);
			return Response.status(Status.NO_CONTENT).build();
		}catch(Exception ex){
			return Response.status(Status.INTERNAL_SERVER_ERROR).entity(Helper.convertToJsonString(new Message(ex.getMessage()))).build();
		}
	}

}

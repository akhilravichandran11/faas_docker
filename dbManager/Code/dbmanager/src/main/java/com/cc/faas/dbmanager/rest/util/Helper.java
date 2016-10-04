package com.cc.faas.dbmanager.rest.util;

import org.codehaus.jackson.map.ObjectMapper;

import com.cc.faas.dbmanager.rest.constants.ExceptionConstants;

public class Helper {
	public static String convertToJsonString(Object obj)
	{
		String output=null;
		if(obj!=null){
			ObjectMapper mapper = new ObjectMapper();
			try {
				output=mapper.writeValueAsString(obj);
			} catch (Exception e) {
				//Do nothing; Return
			} 
		}
		return output;
	}
	public static boolean checkBadRequest(Exception ex) {
		String msg = ex.getMessage();
		if(ExceptionConstants.ID_NOT_IN_DB.equals(msg) || ExceptionConstants.NAME_IN_DB.equals(msg)){
			return true;
		}
		return false;
	}
}

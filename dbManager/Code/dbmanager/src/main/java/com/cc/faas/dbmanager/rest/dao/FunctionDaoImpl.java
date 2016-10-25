package com.cc.faas.dbmanager.rest.dao;

import java.util.ArrayList;
import java.util.List;

import org.hibernate.Query;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.Transaction;

import com.cc.faas.dbmanager.rest.entity.FunctionEntity;

public class FunctionDaoImpl {
	public void createFunction(FunctionEntity functionToSave) throws Exception {
		SessionFactory sessionFactory = HibernateUtil.getSessionFactory();
		Session session = sessionFactory.openSession();
		Transaction tx=null;
		try {
			tx= session.beginTransaction();
			session.save(functionToSave);
			tx.commit();
		} catch(Exception e) {
			if(tx!=null)
				tx.rollback();
			throw e;
		} finally{
			session.close();
		}	
	}
	
	public FunctionEntity findById(String id) throws Exception {
		FunctionEntity foundEntity=null;
		SessionFactory sessionFactory = HibernateUtil.getSessionFactory();
		Session session = sessionFactory.openSession();
		Transaction tx=null;
		try {
			tx= session.beginTransaction();
			Query query = session.createQuery("from FunctionEntity where id = :userid ");
			query.setParameter("userid", id);
			@SuppressWarnings("unchecked")
			List<FunctionEntity> list = (List<FunctionEntity>)query.list();
			if(list != null && !list.isEmpty())
			foundEntity=list.get(0);
			tx.commit();
		} catch(Exception e) {
			if(tx!=null)
				tx.rollback();
			throw e;
		} finally{
			session.close();
		}
		return foundEntity;
	}
		
	public List<FunctionEntity> getAll() throws Exception {
		List<FunctionEntity> allEntities=new ArrayList<FunctionEntity>();
		SessionFactory sessionFactory = HibernateUtil.getSessionFactory();
		Session session = sessionFactory.openSession();
		Transaction tx=null;
		try {
			tx= session.beginTransaction();
			Query query = session.createQuery("from FunctionEntity");
			@SuppressWarnings("unchecked")
			List<FunctionEntity> list = (List<FunctionEntity>)query.list();
			if(list != null && !list.isEmpty())
			allEntities.addAll(list);
			tx.commit();
		} catch(Exception e) {
			if(tx!=null)
				tx.rollback();
			throw e;
		} finally{
			session.close();
		}
		return allEntities;
	}
	
	public FunctionEntity findByNameAndUserId(String userid,String functionName) throws Exception {
		FunctionEntity foundEntity=null;
		SessionFactory sessionFactory = HibernateUtil.getSessionFactory();
		Session session = sessionFactory.openSession();
		Transaction tx=null;
		try {
			tx= session.beginTransaction();
			Query query = session.createQuery("from FunctionEntity where user.id = :userid and name = :functionname");
			query.setParameter("userid", userid);
			query.setParameter("functionname", functionName);
			@SuppressWarnings("unchecked")
			List<FunctionEntity> list = (List<FunctionEntity>)query.list();
			if(list != null && !list.isEmpty())
			foundEntity=list.get(0);
			tx.commit();
		} catch(Exception e) {
			if(tx!=null)
				tx.rollback();
			throw e;
		} finally{
			session.close();
		}
		return foundEntity;
	}
	
	public void updateFunction(FunctionEntity functionToUpdate) throws Exception {
		SessionFactory sessionFactory = HibernateUtil.getSessionFactory();
		Session session = sessionFactory.openSession();
		Transaction tx=null;
		try {
			tx= session.beginTransaction();
			session.update(functionToUpdate);
			tx.commit();
		} catch(Exception e) {
			if(tx!=null)
				tx.rollback();
			throw e;
		} finally{
			session.close();
		}		
	}
	
	public void deleteFunction(String id) throws Exception {
		SessionFactory sessionFactory = HibernateUtil.getSessionFactory();
		Session session = sessionFactory.openSession();
		Transaction tx=null;
		try {
			tx= session.beginTransaction();
			FunctionEntity functionToDelete = (FunctionEntity) session.load(FunctionEntity.class, id);
			session.delete(functionToDelete);
			tx.commit();
		} catch(Exception e) {
			if(tx!=null)
				tx.rollback();
			throw e;
		} finally{
			session.close();
		}
	}

}

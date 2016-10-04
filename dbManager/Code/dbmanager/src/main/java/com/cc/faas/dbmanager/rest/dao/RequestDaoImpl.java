package com.cc.faas.dbmanager.rest.dao;

import java.util.ArrayList;
import java.util.List;

import org.hibernate.Query;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.Transaction;

import com.cc.faas.dbmanager.rest.entity.RequestEntity;

public class RequestDaoImpl {
	public void createRequest(RequestEntity requestToSave) throws Exception {
		SessionFactory sessionFactory = HibernateUtil.getSessionFactory();
		Session session = sessionFactory.openSession();
		Transaction tx=null;
		try {
			tx= session.beginTransaction();
			session.save(requestToSave);
			tx.commit();
		} catch(Exception e) {
			if(tx!=null)
				tx.rollback();
			throw e;
		} finally{
			session.close();
		}	
	}
	
	public RequestEntity findById(String id) throws Exception {
		RequestEntity foundEntity=null;
		SessionFactory sessionFactory = HibernateUtil.getSessionFactory();
		Session session = sessionFactory.openSession();
		Transaction tx=null;
		try {
			tx= session.beginTransaction();
			Query query = session.createQuery("from RequestEntity where id = :userid ");
			query.setParameter("userid", id);
			@SuppressWarnings("unchecked")
			List<RequestEntity> list = (List<RequestEntity>)query.list();
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
		
	public List<RequestEntity> getAll() throws Exception {
		List<RequestEntity> allEntities=new ArrayList<RequestEntity>();
		SessionFactory sessionFactory = HibernateUtil.getSessionFactory();
		Session session = sessionFactory.openSession();
		Transaction tx=null;
		try {
			tx= session.beginTransaction();
			Query query = session.createQuery("from RequestEntity");
			@SuppressWarnings("unchecked")
			List<RequestEntity> list = (List<RequestEntity>)query.list();
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
	
	public void updateRequest(RequestEntity requestToUpdate) throws Exception {
		SessionFactory sessionFactory = HibernateUtil.getSessionFactory();
		Session session = sessionFactory.openSession();
		Transaction tx=null;
		try {
			tx= session.beginTransaction();
			session.update(requestToUpdate);
			tx.commit();
		} catch(Exception e) {
			if(tx!=null)
				tx.rollback();
			throw e;
		} finally{
			session.close();
		}		
	}
	
	public void deleteRequest(String id) throws Exception {
		SessionFactory sessionFactory = HibernateUtil.getSessionFactory();
		Session session = sessionFactory.openSession();
		Transaction tx=null;
		try {
			tx= session.beginTransaction();
			RequestEntity requestToDelete = (RequestEntity) session.load(RequestEntity.class, id);
			session.delete(requestToDelete);
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

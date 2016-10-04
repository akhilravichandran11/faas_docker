package com.cc.faas.dbmanager.rest.dao;

import java.util.ArrayList;
import java.util.List;

import org.hibernate.Query;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.Transaction;

import com.cc.faas.dbmanager.rest.entity.UserEntity;

public class UserDaoImpl {

	public void createUser(UserEntity userToSave) throws Exception {
		SessionFactory sessionFactory = HibernateUtil.getSessionFactory();
		Session session = sessionFactory.openSession();
		Transaction tx=null;
		try {
			tx= session.beginTransaction();
			session.save(userToSave);
			tx.commit();
		} catch(Exception e) {
			if(tx!=null)
				tx.rollback();
			throw e;
		} finally{
			session.close();
		}	
	}
	
	public UserEntity findById(String id) throws Exception {
		UserEntity foundEntity=null;
		SessionFactory sessionFactory = HibernateUtil.getSessionFactory();
		Session session = sessionFactory.openSession();
		Transaction tx=null;
		try {
			tx= session.beginTransaction();
			Query query = session.createQuery("from UserEntity where id = :userid ");
			query.setParameter("userid", id);
			@SuppressWarnings("unchecked")
			List<UserEntity> list = (List<UserEntity>)query.list();
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
	
	public UserEntity findByName(String name) throws Exception {
		UserEntity foundEntity=null;
		SessionFactory sessionFactory = HibernateUtil.getSessionFactory();
		Session session = sessionFactory.openSession();
		Transaction tx=null;
		try {
			tx= session.beginTransaction();
			Query query = session.createQuery("from UserEntity where name = :username ");
			query.setParameter("username", name);
			@SuppressWarnings("unchecked")
			List<UserEntity> list = (List<UserEntity>)query.list();
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
	
	public List<UserEntity> getAll() throws Exception {
		List<UserEntity> allEntities=new ArrayList<UserEntity>();
		SessionFactory sessionFactory = HibernateUtil.getSessionFactory();
		Session session = sessionFactory.openSession();
		Transaction tx=null;
		try {
			tx= session.beginTransaction();
			Query query = session.createQuery("from UserEntity");
			@SuppressWarnings("unchecked")
			List<UserEntity> list = (List<UserEntity>)query.list();
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
	
	public void updateUser(UserEntity userToUpdate) throws Exception {
		SessionFactory sessionFactory = HibernateUtil.getSessionFactory();
		Session session = sessionFactory.openSession();
		Transaction tx=null;
		try {
			tx= session.beginTransaction();
			session.update(userToUpdate);
			tx.commit();
		} catch(Exception e) {
			if(tx!=null)
				tx.rollback();
			throw e;
		} finally{
			session.close();
		}		
	}
	
	public void deleteUser(String userId) throws Exception {
		SessionFactory sessionFactory = HibernateUtil.getSessionFactory();
		Session session = sessionFactory.openSession();
		Transaction tx=null;
		try {
			tx= session.beginTransaction();
			UserEntity userToDelete = (UserEntity) session.load(UserEntity.class, userId);
			session.delete(userToDelete);
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

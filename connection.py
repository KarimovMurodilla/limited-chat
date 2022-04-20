import sqlite3 as sql

class Sqlither:
	def __init__(self, db_file):
		"""Initialization"""
		self.con = sql.connect(db_file)
		self.cur = self.con.cursor()

	# For users table
	def checkUser(self, user_id):
		"""
		We check the user in the database, if the user is not in the users table, 
		then we will register it in the database.
		"""
		with self.con:
			user = self.cur.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,)).fetchone()

			if not user:
				self.cur.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
				self.con.commit()

			return user

	def add_count(self, user_id):
		with self.con:
			self.cur.execute("UPDATE users SET msg_count=msg_count+1 WHERE user_id = ?", (user_id,))
			self.con.commit()


	def get_count(self, user_id):
		with self.con:
			count = self.cur.execute("SELECT msg_count FROM users WHERE user_id = ?", (user_id,)).fetchone()

		try:	
			return count[0]
		except IndexError:
			return None

	def reset_count(self, user_id):
		with self.con:
			self.cur.execute("UPDATE users SET msg_count=0 WHERE user_id = ?", (user_id,))
			self.con.commit()
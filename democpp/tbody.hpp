#ifndef NEURON_SCHEMA_TBODY_HPP
#define NEURON_SCHEMA_TBODY_HPP

#include <string>

#include "dbresult.hpp"
#include "dbsafeutils.hpp"

using namespace std;
using namespace dbquery;

namespace neuronSchema {

class tBody : public DBResult
{
	public:
		tBody(pqxx::connection * db);
		tBody(pqxx::connection * db, const int primaryKey);
		tBody(pqxx::connection * db, int id, const string & text);
		~tBody(void);
	public:
		//SELECT
		void selectRowSQL(pqxx::work* txn);
		//DELETE
		void deleteRowSQL(pqxx::work* txn, int primaryKey);
		//UPDATE
		void updateRowSQL(pqxx::work* txn);
		//INSERT
		void insertRowSQL(pqxx::work* txn);
		//Schema Functions
		//TODO: Figure out how to implement SQL to go down hierarchy
		//shared_ptr<tIndividual> gtIndividuals(void);
	public:
		int 		id;
		string		text;
};
}
#endif //NEURON_SCHEMA_TBODY_HPP

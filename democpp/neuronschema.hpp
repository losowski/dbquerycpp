#ifndef NEURONSCHEMA_HPP
#define NEURONSCHEMA_HPP

#include "dbtransaction.hpp"
#include "dbconnection.hpp"
#include "dbschemabase.hpp"

#include "tbody.hpp"
#include "tindividual.hpp"
using namespace std;
using namespace dbquery;
namespace neuronSchema
{

typedef map < int , ptbody > maptbody;
typedef map < int , ptindividual > maptindividual;

class neuronSchema : public dbquery::DBSchemaBase
{
	public:
		neuronSchema (DBConnection & connection, DBTransaction * transaction);
	public:
		~neuronSchema (void);

	public:
		//Prepare Initailise
		void initialise(void);
		//Purge Cached Objects
		void purgeCachedObjects(void);
		//Get single child objects
		ptbody gettbody(int id, string name);
		ptbody gtbody(int primaryKey);
		ptbody inserttbody(string name);
		paptbody getMultipletbody(string & sqlWhereClause);
		void deletebody(int primaryKey);
		ptindividual gettindividual(int body_id, int id, string name);
		ptindividual gtindividual(int primaryKey);
		ptindividual inserttindividual(int body_id, string name);
		paptindividual getMultipletindividual(string & sqlWhereClause);
		void deleteindividual(int primaryKey);
	private:
		maptbody						tbodyMap;
		maptindividual					tindividualMap;
};


}
#endif //NEURONSCHEMA_HPP

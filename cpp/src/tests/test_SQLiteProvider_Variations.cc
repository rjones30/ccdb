#pragma warning(disable:4800)
#include "tests/catch.hpp"
#include "tests/tests.h"

#include "CCDB/Providers/SQLiteDataProvider.h"
#include "CCDB/Model/Variation.h"

using namespace std;
using namespace ccdb;

/********************************************************************* ** 
 * @brief Test of directories work
 *
 * @return true if test passed
 */
TEST_CASE("CCDB/SQLiteDataProvider/Vars","Varests")
{	
	DataProvider *prov = new SQLiteDataProvider();
	prov->Connect(TESTS_SQLITE_STRING);

	//lets try to get default variation
	Variation *variation = prov->GetVariation("default");
	REQUIRE(variation!=NULL);
	
	//lets get all variations for table 
	//vector<Variation *> variations;
	//bool result = prov->GetVariations(variations, "/test/test_vars/test_table");
	
	//REQUIRE(result);
	//REQUIRE(variations.size()>0);
}


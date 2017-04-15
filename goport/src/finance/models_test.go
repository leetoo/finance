package finance

import (
	"fmt"
	"testing"
)

func TestCreateTables(t *testing.T) {
	db := ConnectDatabase()
	CreateTables(db)
}

func TestInsertAsset(t *testing.T) {
	db := ConnectDatabase()
	asset, errors := InsertAsset(db, "KRW", "Korean Won")

	if len(errors) > 0 {
		t.Error(errors)
	}
	if asset.Name != "KRW" {
		t.Error("Asset was not properly inserted")
	}
}

func TestGetAssetByName(t *testing.T) {
	db := ConnectDatabase()
	asset := GetAssetByName(db, "KRW")
	if asset == (Asset{}) {
		t.Error("No such asset found")
	}
	fmt.Println(asset)
}

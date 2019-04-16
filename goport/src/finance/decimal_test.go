package finance

import (
	"fmt"
	"testing"
)

func TestDecimalFromFloat(t *testing.T) {
	params := []struct {
		value    float64
		expected int64
	}{
		{0.0, 0},
		{0.2345, 2345},
		{1.3825, 13825},
		{17.0000, 170000},
		{845923.4952, 8459234952},
	}

	for _, param := range params {
		actual := DecimalFromFloat(param.value)
		expected := Decimal(param.expected)
		assertEquals(t, expected, actual, "Incorrect value")
	}
}
func TestDecimalFloor(t *testing.T) {
	params := []struct {
		value    int64
		expected int64
	}{
		{-10001, -2},
		{-10000, -1},
		{-9999, -1},
		{-1, -1},
		{0, 0},
		{10000, 1},
		{12345, 1},
	}

	for _, param := range params {
		actual := Decimal(param.value).Floor()
		assertEquals(t, param.expected, actual, fmt.Sprintf("Case %d", param.value))
	}
}

func TestDecimalCeil(t *testing.T) {
	params := []struct {
		value    int64
		expected int64
	}{
		{-10001, -1},
		{-10000, -1},
		{-9999, 0},
		{-1, 0},
		{0, 0},
		{10000, 1},
		{12345, 2},
	}

	for _, param := range params {
		actual := Decimal(param.value).Ceil()
		assertEquals(t, param.expected, actual, fmt.Sprintf("Case %d", param.value))
	}
}

func TestDecimalRound(t *testing.T) {
	params := []struct {
		value    int64
		expected int64
	}{
		{10000, 1},
		{12345, 1},
		{15345, 2},
	}

	for _, param := range params {
		actual := Decimal(param.value).Round()
		assertEquals(t, param.expected, actual, "Incorrect value")
	}
}

func TestAsFloat64(t *testing.T) {
	params := []struct {
		value    int64
		expected float64
	}{
		{10000, 1.0},
		{12345, 1.2345},
		{8459492, 845.9492},
	}

	for _, param := range params {
		actual := Decimal(param.value).AsFloat()
		assertEquals(t, param.expected, actual, "Incorrect value")
	}
}

func TestDecimalArithmatics(t *testing.T) {
	params := []struct {
		x        float64
		y        float64
		expected float64
	}{
		{3.78, 12.3, 16.08},
	}
	for _, param := range params {
		x := DecimalFromFloat(param.x)
		y := DecimalFromFloat(param.y)
		assertEquals(t, DecimalFromFloat(param.expected), x+y, "Incorrect value")
	}
}
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

func TestDecimalWithFormatString(t *testing.T) {
	expected := "863819.0285"
	actual := fmt.Sprintf("%s", DecimalFromString(expected))
	assertEquals(t, expected, actual, "Incorrect value")
}

func TestMul(t *testing.T) {
	params := []struct {
		x        string
		y        string
		expected string
	}{
		{"0.0", "0.0", "0.0"},
		{"0.1", "0.0", "0.0"},
		{"1", "1", "1"},
		{"1", "2", "2"},
		{"2", "2", "4"},
		{"13", "29", "377"},
		{"-7", "19", "-133"},
		{"-23", "-37", "851"},
		{"0.02", "0.04", "0.0008"},
		{"12.01", "-18.75", "-225.1875"},
	}

	for _, param := range params {
		actual := DecimalFromString(param.x).Mul(DecimalFromString(param.y))
		assertEquals(t, DecimalFromString(param.expected), actual,
			fmt.Sprintf("Case %s*%s", param.x, param.y))
	}
}

func TestDiv(t *testing.T) {
	params := []struct {
		x        string
		y        string
		expected string
	}{
		{"0.0", "1.0", "0.0"},
		{"0.3", "0.2", "1.5"},
		{"1", "1", "1"},
		{"2", "2", "1"},
		{"1", "2", "0.5"},
		{"13", "25", "0.52"},
		{"-65659.429", "1994", "-32.9285"},
	}

	for _, param := range params {
		actual := DecimalFromString(param.x).Div(DecimalFromString(param.y))
		assertEquals(t, DecimalFromString(param.expected), actual,
			fmt.Sprintf("Case %s/%s", param.x, param.y))
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
		{-10001, -1},
		{-10000, -1},
		{-5001, -1},
		{-5000, 0},
		{-1, 0},
		{0, 0},
		{5000, 0},
		{5001, 1},
		{10000, 1},
		{12345, 1},
	}

	for _, param := range params {
		actual := Decimal(param.value).Round()
		assertEquals(t, param.expected, actual, fmt.Sprintf("Case %d", param.value))
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
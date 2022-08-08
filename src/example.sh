#!/bin/bash
export ISOTOPES="../dictionaries/isotopes.pz"
export ELEMENTS="../dictionaries/elements.pz"

echo "=================================================="
echo "         Test Isotopes"
echo "=================================================="
python3 isotopes.py
echo ""
echo ""
echo ""

echo "=================================================="
echo "         Test Elements"
echo "=================================================="
python3 elements.py
echo ""
echo ""
echo ""

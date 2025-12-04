import unittest
import os
import shutil
from pathlib import Path
from app import create_app

class BasicTests(unittest.TestCase):
    def setUp(self):
        # create temp data folder inside tests/tmp_data
        self.tmp = Path.cwd() / "src" / "data_test_tmp"
        if self.tmp.exists():
            shutil.rmtree(self.tmp)
        self.tmp.mkdir(parents=True, exist_ok=True)

        # copy sample data from src/data if exists, else run setup_db
        src_data = Path.cwd() / "src" / "data"
        if not src_data.exists():
            # let setup_db create minimal data
            from setup_db import DATA_DIR
        else:
            for f in src_data.glob("*.csv"):
                shutil.copy(f, self.tmp / f.name)

        self.app = create_app({'DATA_PATH': str(self.tmp), 'TESTING': True, 'SECRET_KEY': 'test'})
        self.client = self.app.test_client()

    def tearDown(self):
        if self.tmp.exists():
            shutil.rmtree(self.tmp)

    def test_home_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'EasePharma', response.data)

    def test_admin_protected(self):
        response = self.client.get('/admin/dashboard', follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_add_to_cart_and_cart_page(self):
        # ensure at least one product exists
        rv = self.client.get('/')
        self.assertEqual(rv.status_code, 200)
        # find product id by parsing generated page (simple approach)
        # instead, call product model directly
        from app.models.product_model import ProductModel
        products = ProductModel.get_all(str(self.tmp))
        if not products:
            self.skipTest("No products to test cart")
        pid = products[0].id
        # post add to cart
        res = self.client.post(f'/add_to_cart/{pid}', follow_redirects=True)
        self.assertIn(b'Item added to cart', res.data)
        res2 = self.client.get('/cart')
        self.assertIn(products[0].name.encode(), res2.data)

if __name__ == "__main__":
    unittest.main()

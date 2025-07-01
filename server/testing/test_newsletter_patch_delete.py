import unittest
from server.app import app, db
from server.models import Newsletter

class NewsletterPatchDeleteTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
            # Add a sample newsletter
            newsletter = Newsletter(title='Test Title', body='Test Body')
            db.session.add(newsletter)
            db.session.commit()
            self.newsletter_id = newsletter.id

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_patch_newsletter(self):
        # Update title and body
        response = self.client.patch(f'/newsletters/{self.newsletter_id}', data={
            'title': 'Updated Title',
            'body': 'Updated Body'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['title'], 'Updated Title')
        self.assertEqual(data['body'], 'Updated Body')

    def test_patch_newsletter_invalid_field(self):
        # Attempt to update a non-existent field
        response = self.client.patch(f'/newsletters/{self.newsletter_id}', data={
            'nonexistent': 'value'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        # The invalid field should be ignored, original fields unchanged
        self.assertNotIn('nonexistent', data)

    def test_delete_newsletter(self):
        response = self.client.delete(f'/newsletters/{self.newsletter_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'record successfully deleted')
        # Verify deletion
        get_response = self.client.get(f'/newsletters/{self.newsletter_id}')
        self.assertEqual(get_response.status_code, 404)  # Updated to expect 404

    def test_delete_nonexistent_newsletter(self):
        response = self.client.delete('/newsletters/9999')
        self.assertEqual(response.status_code, 404)  # Updated to expect 404

if __name__ == '__main__':
    unittest.main()

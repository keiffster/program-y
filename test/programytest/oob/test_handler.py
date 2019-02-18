
"""
    def test_oob_stripping(self):

        yaml = YamlConfigurationFile()
        self.load_os_specific_configuration(yaml, "test_brain.yaml", "test_brain.windows.yaml")

        brain_config = BrainConfiguration()
        brain_config.load_configuration(yaml, ".")

        client = TestClient()
        client_context = client.create_client_context("testid")
        brain = Brain(client_context.bot, brain_config)

        response, oob = brain.strip_oob("<oob>command</oob>")
        self.assertEqual("", response)
        self.assertEqual("<oob>command</oob>", oob)

        response, oob = brain.strip_oob("This <oob>command</oob>")
        self.assertEqual("This ", response)
        self.assertEqual("<oob>command</oob>", oob)

        response, oob = brain.strip_oob("This <oob>command</oob> That")
        self.assertEqual("This That", response)
        self.assertEqual("<oob>command</oob>", oob)

    def test_oob_processing(self):

        yaml = YamlConfigurationFile()
        self.load_os_specific_configuration(yaml, "test_brain.yaml", "test_brain.windows.yaml")

        brain_config = BrainConfiguration()
        brain_config.load_configuration(yaml, ".")

        client = TestClient()
        client_context = client.create_client_context("testid")
        brain = Brain(client_context.bot, brain_config)

        self.assertEqual("", brain.process_oob("console", "<oob></oob>"))

"""
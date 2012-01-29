from distutils.core import setup
setup(name         = 'pyiqe',
      version      = '1.2.1',
      author       = 'IQ Engines',
      author_email = 'support@iqengines.com',
      description  = "IQ Engines API client",
      keywords     = ["iqengines", "pyiqe", "visual search"],
      url          = "http://github.com/iqengines/pyiqe",
      download_url = "https://github.com/iqengines/pyiqe/tarball/v1.2.1",
      packages     = ['pyiqe','pyiqe.apis', 'pyiqe.apis.api1_2'],
      classifiers  = [
          "Programming Language :: Python",
          "Operating System :: OS Independent",
          "License :: OSI Approved :: BSD License",
          "Intended Audience :: Developers",
          "Development Status :: 5 - Production/Stable",
          "Topic :: Software Development :: Libraries :: Python Modules",
          ],

      long_description = """\
      IQ Engines API Client Bindings
      ------------------------------

      DESCRIPTION
      -----------
      
      Give your applications the power of Visual Search using the IQ Engines
      platform. For more information visit http://developer.iqengines.com/

      USAGE
      -----
      
      For more documentation see https://github.com/iqengines/pyiqe
      
      """
      )



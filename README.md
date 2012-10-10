eprints_webservices
===================

Plug-ins for e-Prints that is intended for reception of records under protocol SOAP (http://www.w3.org/TR/soap/).

Original scripts from http://files.eprints.org/383/

= Features =

1. Service acquisition metadata about id item MetaDataServ (return metadata for item id)

2. Service find item, the service allows us to search datasets for data objects matching specific criteria. (return list id item for pair keyword and list fields)

3. Service deposit item, the service allows deposits to a repository

= Requirements =

1. Install SOAP::Lite from cpan (http://search.cpan.org/~mkutter/SOAP-Lite-0.710.08/)

2. Configure auto-apache.conf having added in existing virtual a host the following:

```


/path_to_eprints/archives/archive_id/var/auto-apache.conf

section <VirtualHost>  must have 
.
.
.

   <Directory "/path_to_eprints/cgi/soap/">

   SetHandler perl-script
   PerlHandler ModPerl::Registry
   PerlHandler Apache::Registry
   PerlSendHeader On
   Options ExecCGI FollowSymLinks
   PerlHandler ServerDemo
   PerlOptions +GlobalRequest
   AddHandler cgi-script .cgi
   AllowOverride None
   Options ExecCGI FollowSymLinks
   Order allow,deny
   Allow from all
   </Directory>

.
.
.
</VirtualHost>



= Installation =

1. Create directory in your ePrints directory: /eprints/cgi/soap

2. In this directory copy the cgi scripts: SearchServ.cgi MetaDataServ.cgi

3. Create directory /eprints/archives/{your archive id}/html/{your default languge}/wsdl

4. In this directory copy the wsdl files: MetaDataServ2.wsdl SearchServ2.wsdl putEprints2.wsdl

5. Replace in MetaDataServ2.wsdl SearchServ2.wsdl putEprints2.wsdl string you.domain with your domain 
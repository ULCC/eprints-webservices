#!/usr/bin/perl

package putEprint;

use lib '/opt/eprints3/perl_lib';

use EPrints;
use EPrints::DataObj::EPrint;
use Data::Dumper;
use Encode;
use Unicode::String qw( utf8 );
use MIME::Base64;
use LWP::Simple;


sub putEprint {

    # input id metadata
    my ($self, $title, $creators_name, $date,  $abstract, $url_file, $type) = @_;

    #need set repo id
#    my $session = new EPrints::Session;
     my $session = new EPrints::Session( 1, 'ualoer');
     exit(0) unless ( defined $session );

    # Get archive dataset
    my $dataset = $session->get_repository->get_dataset("archive");

    # Create new eprint
    my $eprint = EPrints::DataObj::EPrint::create( $session, $dataset );


# my $listid=SOAP::Data->name('status')->type('ArrayOfstring')->value(\@creators_name);

# my $listid=SOAP::Data->name('id2')->type('string')->value(ref(\@creators_name));
open( MYFILE, '>>/usr/share/eprints3/cgi/soap/data.txt' );


@creators_name=$creators_name;
print MYFILE Dumper(@creators_name);
    foreach $creator ( @{ \@creators_name } ) {

        foreach $items ($creator->{item}) {

       #one creators
        if (ref($items) eq 'HASH'){
       
           $eprint->set_value("creators_name",    [$creator->{item}]);
        }

       #more creators
       if (ref($items) eq 'ARRAY')
           {
            @creatorItem=$creator->{item};
            $eprint->set_value("creators_name",    @creatorItem);
            }
     #       print MYFILE Dumper(ref($items));
        }
        
    


#print MYFILE Dumper( $creator);
#print MYFILE Dumper( ref($creator));
#print MYFILE Dumper( $creator->{item});
#  foreach $items ($creator->{item}) {
#            foreach $item ( @{$items} ) {
#                    print MYFILE Dumper(bless ($creator, Array));
#                    print MYFILE Dumper($item->[0]{given});
#                    print MYFILE Dumper( $item->{given} );
#            }
#        }
       
    }

 
    
 #   $eprint->set_value(
 #       "creators_name",
  #      [
  #          { family => "Smith", given => "John" },
  #          { family => "Jones", given => "Mary" },
   #     ]
  #  );
    $eprint->set_value("title", $title);
    $eprint->set_value("date", $date);
    $eprint->set_value("type", $type);
    $eprint->set_value("status", $type);
    $eprint->commit();
 #print MYFILE Dumper($title);
 # print MYFILE Dumper($url_file);

    # Add document to eprint
    my $pdf;
    my $doc_file = $url_file;
    $doc_file_name = 'eprints.pdf';
    if ( open( $pdf, $doc_file ) ) {
        my $doc = EPrints::DataObj::Document::create( $session, $eprint );
        $doc->add_file( $doc_file, "$doc_file_name" );
        $doc->set_value( "format", "application/pdf" );
        close $pdf;
        $doc->set_value( "main", $doc_file_name );
        $doc->commit;
    }
    else {
    print MYFILE Dumper("Failed to open file: $filename $!\n");

    }

    # Generate abstract page for new eprint
    $eprint->generate_static;

    #    print "Created EPrint #" . $eprint->get_id . "\n";

    # End session
    $session->terminate();
close(MYFILE);
$listid=SOAP::Data->name('status')->type('string')->value('ok');
    return $listid;

    # start session Eprints
 

}

package main;

use SOAP::Lite +trace;
use SOAP::Transport::HTTP;

# set ecnvoding all data
#*SOAP::Serializer::as_string =
#  \&SOAP::XMLSchema2001::Serializer::as_base64Binary;

#SOAP::Transport::HTTP::CGI->dispatch_to('putEprint')->handle;

#1;


  # don't want to die on 'Broken pipe' or Ctrl-C
  $SIG{PIPE} = $SIG{INT} = 'IGNORE';

  my $daemon = SOAP::Transport::HTTP::Daemon
	-> new (LocalPort => 1024)
	-> dispatch_to('putEprint');

  print "Contact to SOAP server at ", $daemon->url, "\n";
  $daemon->handle;






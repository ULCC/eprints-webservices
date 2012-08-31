#!/usr/bin/perl

package MetaDataServ;

use EPrints; 
use EPrints::DataObj::EPrint;
use Data::Dumper;
use Encode;

use MIME::Base64;


sub getEprint
    {

    # input id of eprint object
    my( $self, $id) = @_;
    
    # start session Eprints
    my $session = new EPrints::Session;  
    exit( 0 ) unless( defined $session );
    my $ds = $session->get_repository->get_dataset( "archive" );

    my $eprint = EPrints::DataObj::EPrint->new( $session, $id); 
    if (!defined $eprint) {return "not found ID"; exit(0)};

    #get metadata for concrete eprints object
    my %metadata;
    $metadata{'title'} = $eprint->get_value( "title" );
    $metadata{'type'} = $eprint->get_value( "type" );
    $metadata{'abstract'} = $eprint->get_value( "abstract" );
    $metadata{'keywords'} = $eprint->get_value( "keywords" ); 
    $metadata{'datecontr'} = $eprint->get_value( "datecontr" );
    $metadata{'creators'} = $eprint->get_value( "creators" );
    $metadata{'ispublished'} = $eprint->get_value( "ispublished" );
    $metadata{'subjects'} = $eprint->get_value( "subjects" );
    $metadata{'date'} = $eprint->get_value( "date" );
    $metadata{'series'} = $eprint->get_value( "series" );
    $metadata{'publication'} = $eprint->get_value( "publication" );
    $metadata{'volume'} = $eprint->get_value( "volume" );
    $metadata{'number'} = $eprint->get_value( "number" );
    $metadata{'pages'} = $eprint->get_value( "pages" );
    $metadata{'isbn'} = $eprint->get_value( "isbn" );
    $metadata{'issn'} = $eprint->get_value( "issn" );
    $metadata{'book_title'} = $eprint->get_value( "book_title" );
    $metadata{'editors'} = $eprint->get_value( "editors" );

    ## preparation of values is for sending
    
    
#    work
    my $title=SOAP::Data->name('title')->type('string')->value($metadata{'title'});
    
    
    my @all_creators=@{$metadata{'creators'}};
    my $count=@all_creators;
    my $i=0;
    while ($i<$count) {
      $result_creators[$i]->{'creators'}{'id'}=SOAP::Data->name('id')->value($metadata{'creators'}[$i]{'id'});
      $result_creators[$i]->{'creators'}{'name'}{'given'} = SOAP::Data->name('given')->value($metadata{'creators'}[$i]{'name'}{'given'});
      $result_creators[$i]->{'creators'}{'name'}{'family'} =SOAP::Data->name('family')->value($metadata{'creators'}[$i]{'name'}{'family'});
      $i++;
    }
    my $creators = SOAP::Data->value(@result_creators);
    my $type=SOAP::Data->name('type')->value($metadata{'type'});
    my $abstract=SOAP::Data->name('abstract')->type('string')->value($metadata{'abstract'});
    my $r=$session->get_repository->get_conf("base_url");
    $r.='/'.$eprint->get_value( "eprintid" ); 
    my $relation=SOAP::Data->name('relation')->value($r);
    my $keywords=SOAP::Data->name('keywords')->type('string')->value($metadata{'keywords'});
    my $datecontr=SOAP::Data->name('datecontr')->type('string')->value($metadata{'datecontr'});
    
    
 
     
    
    my @all_subjects=@{$metadata{'subjects'}};
    my $count_sub=@all_subjects;
    my $j=0;
    while ($j<$count_sub)
    {
    $result_subjects[$j]=get_subject_name_string ($session, $metadata{'subjects'}[$j]);
    $j++;
    
    }
   
    my $subjects=SOAP::Data->name('subjects')->type('ArrayOfString')->value(\@result_subjects);
  
  
    #return all vallues
    return ($title, $creators, $type, $abstract, $relation, $keywords, $datecontr, $subjects);

sub get_subject_name_string
 { 
  my( $session, $subjectid ) = @_; 
   my $subj = EPrints::Subject->new( $session, $subjectid ); 
    if( !defined $subj ) 
     { 
  return "errer, unknown subject: $subjectid"; 
       } 
        return EPrints::Utils::tree_to_utf8($subj->render_description() );
		
	
 } 
}

package main;

use SOAP::Lite +trace;
use SOAP::Transport::HTTP;

SOAP::Transport::HTTP::CGI
->dispatch_to( 'MetaDataServ')
->handle;

1;


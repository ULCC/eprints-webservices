#!/usr/bin/perl

package MetaDataServ;

use EPrints; 
use EPrints::DataObj::EPrint;
use Data::Dumper;
use Encode;
use Unicode::String qw( utf8 );  
use MIME::Base64;
use utf8;
no utf8;



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

    #get metadata for ecth  eprints object
    my %metadata;
    $metadata{'title'} = $eprint->get_value( "title" );
    $metadata{'type'} = $eprint->get_value( "type" );
    $metadata{'abstract'} = $eprint->get_value( "abstract" );
    $metadata{'keywords'} = $eprint->get_value( "keywords" ); 
    $metadata{'datecontr'} = $eprint->get_value( "datecontr" );
    $metadata{'creators'} = $eprint->get_value( "creators_name" );
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

   # read creators name in array
   my $creators = $eprint->get_value( "creators_name" );
		if( defined $creators )
		{
			foreach my $creator ( @{$creators} )
			{
				next if !defined $creator;
				push @metadata, [ "creator", EPrints::Utils::make_name_string( $creator ) ];
			}
		}
#    $metadata{'creators_list'}

#    work

# function define encoding utf-8 for each metadata

sub conve_utf8
{
 my($sting_utf8) = @_;

 my $sting_utf8  = pack 'U*', unpack 'U0U*', $sting_utf8;
 
 #my $sting_utf8  =  $sting_utf8;
 
 return $sting_utf8;
}

# function get line subjects

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

# tranlate all data array to utf-8


foreach $value_metadata (keys %metadata)
{
   $metadata{$value_metadata}=conve_utf8($metadata{$value_metadata});
}
 




# work   
my $title=SOAP::Data->name('title')->type('string')->value($metadata{'title'});


# my $result_creators=SOAP::Data->name('creators')->type('ArrayOfString')->value(\@result_creators);


#my $test4=conve_utf8($test4);
#SOAP::Serializer::as_string = \&SOAP::XMLSchema2001::Serializer::as_base64Binary;

#my $result_creators=SOAP::Data->name('creators')->type('ArrayOfString')->value(\@result_creators);
# my $result_creators=SOAP::Data->name('creators')->type('ArrayOfString')->value(\@creators);
# my $result_creators = SOAP::Data->name("creators" =>\SOAP::Data->name("name" => \@creators,)->type('string'));


#SOAP::Serializer:an as_sting
#$serialized = SOAP::Serializer->serialize->as_string(
#    SOAP::Data->name(test => \SOAP::Data->value("\0\1\2\3   \4\5\6", "<123>&amp;\015</123>"))
#  );
  
#  SOAP::Serializer:an as_sting
#my $result_creators = SOAP::Serializer->serialize->as_string(SOAP::Data->name('creators')->type('ArrayOfString')->value(\@result_creators));
#SOAP::Serializer::as_string = \&SOAP::XMLSchema2001::Serializer::as_base64Binary;
# my $result_creators = SOAP::Serializer->serialize(SOAP::Data->name('creators')->type('ArrayOfString')->value(\@result_creators));


## work
#    my @all_creators=@{$metadata{'creators'}};
#    my $count=@all_creators;
#    my $i=0;
#    while ($i<$count) {
#      $result_creators[$i]->{'creators'}{'id'}=SOAP::Data->name('id')->value($metadata{'creators'}[$i]{'id'});
#     $result_creators[$i]->{'creators'}{'name'}{'given'} = SOAP::Data->name('given')->value($metadata{'creators'}[$i]{'name'}{'given'});
#     $result_creators[$i]->{'creators'}{'name'}{'family'} =SOAP::Data->name('family')->value($metadata{'creators'}[$i]{'name'}{'family'});
#     $i++;
#    }
    
#   my $creators = SOAP::Data->value(@result_creators);


## end

 # my @all_creators=@{$metadata{'creators'}};
  # my $count=@all_creators;
 #   my $i=0;
 #   while ($i<$count) {
    # push @resultSoap, SOAP::Data->name('result')->type('string')->value('no_subscribers');
     
     
    #  $result_creators[$i]->{'creators'}{'id'}=SOAP::Data->name('id')->value($metadata{'creators'}[$i]{'id'});
   #  push @resultSoap, SOAP::Data->name('id')->value($metadata{'creators'}[$i]{'id'});
     #$result_creators[$i]->{'creators'}{'name'}{'given'} = SOAP::Data->name('given')->value($metadata{'creators'}[$i]{'name'}{'given'});
    #   push @resultSoap, SOAP::Data->name('given')->value($metadata{'creators'}[$i]{'name'}{'given'});
   #    push @resultSoap, SOAP::Data->name('family')->value($metadata{'creators'}[$i]{'name'}{'family'});
   #  $result_creators[$i]->{'creators'}{'name'}{'family'} =SOAP::Data->name('family')->value($metadata{'creators'}[$i]{'name'}{'family'});
  #   $i++;
   # }

# my $creators = SOAP::Data->value(\@result_creators);
    
    
#    my $type=SOAP::Data->name('type')->value($metadata{'type'});
    my $abstract=SOAP::Data->name('abstract')->type('string')->value($metadata{'abstract'});
    
    my $r=$session->get_repository->get_conf("base_url");
    $r.='/'.$eprint->get_value( "eprintid" ); 
    my $relation=SOAP::Data->name('relation')->value($r);
#    my $keywords=SOAP::Data->name('keywords')->type('string')->value($metadata{'keywords'});
#    my $datecontr=SOAP::Data->name('datecontr')->type('string')->value($metadata{'datecontr'});

# get SOAP creators name
    my $creators = $eprint->get_value( "creators_name" );
    
   # my $count_cre=@{$creators};
  open( MYFILE, '>>/usr/share/eprints3/cgi/soap/data.txt' );
    if( defined $creators )
     {
     undef (@result_creators);
          foreach my $creator ( @{$creators} )
   		{
                   #    next if !defined $creator;
                       push @result_creators,  conve_utf8(EPrints::Utils::make_name_string( $creator ));
#                       print MYFILE Dumper(conve_utf8(EPrints::Utils::make_name_string( $creator )));
                }
     }
     
     close(MYFILE);
      my $count_cre=@result_creators;
    my $creators=SOAP::Data->name('creators')->type('ArrayOfString')->value(\@result_creators);
         my $count_cre=SOAP::Data->name('test')->type('string')->value($count_cre);
    
    
# get SOAP subjects
    my $subjects = $eprint->get_value( "subjects" );
		if( defined $subjects )
		{
		  undef (@result_subjects);
			foreach my $subjects ( @{$subjects} )
			{
				next if !defined $subjects;
				push @result_subjects, conve_utf8(get_subject_name_string ($session, $subjects));
			}
		}
    my $subjects=SOAP::Data->name('subjects')->type('ArrayOfString')->value(\@result_subjects);
    
  
  
    #return all vallues
   # return ($title, $creators, $type, $abstract, $relation, $keywords, $datecontr, $subjects);
   return ($title, $subjects, $creators, $abstract, $relation, $count_cre);
 
}

package main;

use SOAP::Lite +trace;
use SOAP::Transport::HTTP;

# set encoding all data
*SOAP::Serializer::as_string = \&SOAP::XMLSchema2001::Serializer::as_base64Binary;
#*SOAP::Serializer::as_string = \&SOAP::XMLSchema2001::Serializer::as_string;
 
SOAP::Transport::HTTP::CGI
->dispatch_to( 'MetaDataServ')
->handle;


1;


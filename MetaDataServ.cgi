#!/usr/bin/perl

package MetaDataServ;

#version 2.0  from 20.10.2012 11:51

use EPrints;
use EPrints::DataObj::EPrint;
use Data::Dumper;
$Data::Dumper::Indent = 1;
use Encode;
use Unicode::String qw( utf8 );
use MIME::Base64;
use utf8;
no utf8;



sub getEprint
    {

    # input id of eprint object
    my( $self, @listId) = @_;


undef @metadata;
undef $resource;
undef @resources;
undef $resources_list;
undef $result;
#use for debug
#   open( MYFILE, '>>/usr/share/eprints3/cgi/soap/data.txt' );
#   print MYFILE Dumper("listId start");
#   print MYFILE Dumper(\@listId);
#   print MYFILE Dumper("listId end");
#   close(MYFILE);



    # start session Eprints
    my $session = new EPrints::Session;
    exit( 0 ) unless( defined $session );
    my $ds = $session->get_repository->get_dataset( "archive" );


 foreach $id_item ( @{ \@listId } ) {
undef @temp;
 #if one id
 if (ref($id_item->{item}) eq ""){
 my %temp;

  push  @temp, $id_item->{item};
 #$id_item->{item}="[\'".$id_item->{item}."\']";

 $id_item->{item} = \@temp;

 }



  foreach $one_id ($id_item->{item}) {
  $arraySize = @{ $one_id };
  my $i=0;
    while ($i<$arraySize)
    {
    
    
    
    
    $id=@{ $one_id }[$i];

    my $eprint = EPrints::DataObj::EPrint->new( $session, $id);
   # if (!defined $eprint) {return "not found ID"; exit(0)};





     undef $resources_list;
     undef @result_creators;
     undef $elem1;
     undef $creators;
     undef @result_subjects;
     undef $elem2;
     undef $subjects_list;
     undef @metadata;

    #get creators
     

    my $creators = $eprint->get_value( "creators_name" );

    if( defined $creators )
     {

          foreach my $creator ( @{$creators} )
   		{
                       next if !defined $creator;
                      $elem1 = SOAP::Data->name('item' => EPrints::Utils::make_name_string( $creator ))->type('string');
                      push(@result_creators, $elem1);
                }
     }

    $creators_list = SOAP::Data
        ->name("CreatorsList" => \SOAP::Data->value(

              SOAP::Data->name("someArray" => \SOAP::Data->value(
                  SOAP::Data->name("someArrayItem" => @result_creators)
                            ->type("SomeObject"))
                       )->type("ArrayOf_SomeObject") ))

    ->type("SomeObject");




# get SOAP subjects

    my $subjects = $eprint->get_value( "subjects" );
		if( defined $subjects )
		{

			foreach my $subjects ( @{$subjects} )
			{
				next if !defined $subjects;

				 $elem2 = SOAP::Data->name('item' => get_subject_name_string ($session, $subjects))->type('string');
                              push(@result_subjects, $elem2);
			}
		}

  $subjects_list = SOAP::Data
        ->name("SubjectsList" => \SOAP::Data->value(

              SOAP::Data->name("someArray" => \SOAP::Data->value(
                  SOAP::Data->name("someArrayItem" => @result_subjects)
                            ->type("SomeObject"))
                       )->type("ArrayOf_SomeObject") ))

    ->type("SomeObject");



    my $r=$session->get_repository->get_conf("base_url");
    $r.='/'.$eprint->get_value( "eprintid" );

  # tranlate all data array to utf-8

#    foreach $value_metadata (keys %metadata)
#    {
#            $metadata{$value_metadata}=conve_utf8($metadata{$value_metadata});
#    }

 #push(@myNames, 'Moe');
     push (@metadata, SOAP::Data->name('title')->type('string')->value($eprint->get_value( "title" )));
     push (@metadata, SOAP::Data->name('type')->type('string')->value($eprint->get_value( "type" )) );
     push (@metadata, SOAP::Data->name('abstract')->type('string')->value($eprint->get_value( "abstract" )) );
     push (@metadata, SOAP::Data->name('keywords')->type('string')->value($eprint->get_value( "keywords" )) );
 #    push (@metadata, SOAP::Data->name('datecontr')->type('string')->value($eprint->get_value( "datecontr" )) );
     push (@metadata, SOAP::Data->name('date')->type('string')->value($eprint->get_value( "date" )) );
     push (@metadata, SOAP::Data->name('creators')->value($creators_list) );
     push (@metadata, SOAP::Data->name('subjects')->value($subjects_list) );
     push (@metadata, SOAP::Data->name('relation')->type('anyURI')->value($r) );

# $resources_list = SOAP::Data
#       ->name("ResourcesList" => \SOAP::Data->value(
#
#              SOAP::Data->name("someArray" => \SOAP::Data->value(
#                  SOAP::Data->name("someArrayItem" => @metadata)
#                            ->type("SomeObject"))
#                       )->type("ArrayOf_SomeObject") ))
#
#    ->type("SomeObject");
    
    
    
      $resources_list = SOAP::Data
        ->name("ResourcesList" => \SOAP::Data->value( @metadata ))

    ->type("SomeObject");
    
    
    
    
     $resource = SOAP::Data->value($resources_list)->type('ArrayOf_SomeObject');
push(@resources, $resource);

undef @metadata;
undef $resources_list;
undef $resource;
     $i++;
     }
  }
 }
 
 
 

 $result=SOAP::Data->name('items')->type('ArrayOfItems')->value(\@resources);

#print MYFILE Dumper($result);

 return ($result);

}





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








sub struct_to_soap {
    my ($data, $format) = @_;
    my $soap_data;

    unless (ref($data) eq 'HASH') {
	return undef;
    }

    if ($format eq 'as_string') {
	my @all;
	my $formated_data;
	foreach my $k (keys %$data) {
	    my $one_data = $k.'='.$data->{$k};

	    ## Decode from the current charset to perl internal charset
	    ## Then encode strings to UTF-8
	    if (require "Encode.pm") {
		# $one_data = &Encode::decode(&Language::GetCharset(), $one_data);
		$one_data = &Encode::encode('utf-8', $one_data);
	    }

	    push @all, $one_data;
	}

	$formated_data = join ';', @all;
	$soap_data = SOAP::Data->type('string')->value($formated_data);
    }else {
	my $formated_data;
	foreach my $k (keys %$data) {
	    $formated_data->{$k} = SOAP::Data->name($k)->type($types{'listType'}{$k})->value($data->{$k});
	}

	$soap_data = SOAP::Data->value($formated_data);
    }

    return $soap_data;
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









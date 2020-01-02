#!/usr/bin/perl
#
# Maintained later on by Elan Ruusamäe <glen@pld-linux.org>
# https://github.com/glensc/monitoring-plugin-check_amavis

use Getopt::Long;
use MIME::Entity;
use Net::SMTP;
use strict;
use warnings;

my $server = '';
my $port = 10024;
my $from = '';
my $to = '';
my $debug = 0;
my $timeout = 15;

my %STATES = (
	"OK" => 0,
	"WARNING" => 1,
	"CRITICAL" => 2,
	"UNKNOWN" => 3,
	"DEPENDENT" => 4,
);

GetOptions (
	"server|s=s"    => \$server,
	"port|p=s"      => \$port,
	"from|f=s"      => \$from,
	"timeout=s"     => \$timeout,
	"debug|d"       => \$debug,
	"to|t=s"        => \$to,
);

if (!$server || !$from) {
	print "ERROR: Please specify --server, --from\n";
	exit $STATES{UNKNOWN};
}

if (!$to) {
	$to = $from;
}

my $EICAR = <<'EOF';
X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*
EOF

my $top = MIME::Entity->build(
	Type    => "multipart/mixed",
	From    => $from,
	To      => $to,
	Subject => "EICAR test",
	Data    => "This is a test",
);

$top->attach(
	Data        => $EICAR,
	Type        => "application/x-msdos-program",
	Encoding    => "base64",
);

my $smtp = new Net::SMTP(
	$server,
	Port => $port,
	Debug => $debug,
	Timeout => $timeout,
);

if (!$smtp) {
	print "CRITICAL - amavisd-new server unreachable\n";
	exit $STATES{CRITICAL};
}

$smtp->mail($from);
$smtp->to($to);
$smtp->data();
$smtp->datasend($top->stringify);
$smtp->dataend();
my $result = $smtp->message();
$smtp->close();

warn "RESULT[$result]\n" if $debug;

# <<< 250 2.5.0 Ok, id=21563-09, BOUNCE
if ($result =~ /2\.7\.[01] Ok,/ && $result =~ /discarded|BOUNCE/) {
	print "OK - All fine\n";
	exit $STATES{OK};
} else {
	print "CRITICAL - amavisd-new returned $result\n";
	exit $STATES{CRITICAL};
}
